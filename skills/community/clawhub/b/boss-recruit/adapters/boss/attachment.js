/**
 * BOSS直聘 attachment — 零弹窗下载候选人的「附件简历」PDF。
 *
 * 机制（逆向自 boss 招聘端，全程不开可见 tab）：
 *   1. check.json?geekId=<uid>  → 拿 encryptAuthorityId（用页面内 XHR，带 cookie）
 *   2. 拼 docdownload.zhipin.com/.../download4boss/<uid>?id=<authorityId>
 *   3. page.getCookies (CDP, 含 HttpOnly) + httpDownload(Node 端 undici 直接下载)
 *      —— 页面内 fetch 会被跨子域 CORS 拦，所以走 Node 端，且零弹窗。
 *
 * 用法:
 *   opencli boss attachment <encrypt_uid> [--name 张三] [--output ./dir] [--format json]
 *
 * 返回 status:
 *   downloaded            —— 已下载，file 字段是本地 PDF 路径
 *   no_attachment_visible —— 候选人没有可见的附件简历（去主动要简历）
 */
import { cli, Strategy } from '@jackwener/opencli/registry';
import { CommandExecutionError, AuthRequiredError } from '@jackwener/opencli/errors';
import { httpDownload, formatCookieHeader, sanitizeFilename, getTempDir } from '@jackwener/opencli/download';
import path from 'node:path';
import fs from 'node:fs';

const DOMAIN = 'www.zhipin.com';
const CHECK_URL = `https://${DOMAIN}/wapi/zpgeek/resume/boss/preview/check.json`;
const DOWNLOAD_BASE = 'https://docdownload.zhipin.com/wflow/zpgeek/download/download4boss';
const COOKIE_EXPIRED_CODES = new Set([7, 37]);

/** 页面内带 cookie 的 XHR（同 boss/utils 的 bossFetch 思路），返回解析后的 JSON。 */
async function zpFetch(page, url) {
    const script = `
    async () => new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', ${JSON.stringify(url)}, true);
      xhr.withCredentials = true;
      xhr.timeout = 15000;
      xhr.setRequestHeader('Accept', 'application/json');
      xhr.onload = () => { try { resolve(JSON.parse(xhr.responseText)); } catch (e) { reject(new Error('JSON parse failed')); } };
      xhr.onerror = () => reject(new Error('Network Error'));
      xhr.ontimeout = () => reject(new Error('Timeout'));
      xhr.send(null);
    })`;
    const data = await page.evaluate(script);
    if (!data || typeof data !== 'object') {
        throw new CommandExecutionError('Boss check.json 返回异常');
    }
    return data;
}

cli({
    site: 'boss',
    name: 'attachment',
    access: 'read',
    description: 'BOSS直聘下载候选人附件简历 PDF（零弹窗，Node 端带 cookie 下载）',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    navigateBefore: false,
    browser: true,
    args: [
        { name: 'uid', positional: true, required: true, help: '候选人 encrypt_uid（即 geekId，来自 recommend/chatlist）' },
        { name: 'name', default: '', help: '候选人姓名（仅用于文件名，可选）' },
        { name: 'output', default: '', help: '输出目录（默认系统临时目录）' },
    ],
    columns: ['uid', 'status', 'name', 'file', 'size', 'authority_id', 'detail'],
    func: async (page, kwargs) => {
        const uid = String(kwargs.uid ?? '').trim();
        if (!uid) throw new CommandExecutionError('缺少 uid');
        const name = String(kwargs.name ?? '').trim();

        // 仅当当前不在 zhipin 页面时才导航（保留用户已打开的预览/视图）
        const here = String(await page.evaluate('location.href') || '');
        if (!here.includes('zhipin.com')) {
            await page.goto(`https://${DOMAIN}/web/chat/index`);
            await page.wait({ time: 2 });
        }

        // 1. check.json 拿授权
        const check = await zpFetch(page, `${CHECK_URL}?geekId=${encodeURIComponent(uid)}`);
        if (COOKIE_EXPIRED_CODES.has(check.code)) {
            throw new AuthRequiredError(DOMAIN, 'Cookie 已过期，请在 Chrome 中重新登录 BOSS 直聘招聘端');
        }
        const zp = check.zpData || {};
        const authorityId = zp.encryptAuthorityId || '';
        const visible = zp.isResumeVisible !== false && zp.isCanPreview !== false;
        if (!authorityId || !visible) {
            // 没有可见的附件简历 —— 交给上层走"主动要简历"分支
            return [{
                uid, status: 'no_attachment_visible', name,
                file: '', size: 0, authority_id: '',
                detail: zp.expired ? '简历预览已过期' : '候选人暂无可见的附件简历，需先索要附件简历',
            }];
        }

        // 2. 拼下载链接
        const downloadUrl = `${DOWNLOAD_BASE}/${encodeURIComponent(uid)}?id=${encodeURIComponent(authorityId)}`;

        // 3. 拿 cookie（CDP，含 HttpOnly）→ Node 端下载（零弹窗，无 CORS）
        const cookies = await page.getCookies({ domain: 'zhipin.com' });
        const cookieHeader = formatCookieHeader(cookies);

        const outDir = kwargs.output ? path.resolve(String(kwargs.output)) : getTempDir();
        await fs.promises.mkdir(outDir, { recursive: true });
        const baseName = sanitizeFilename(name ? `${name}_${uid}` : `boss-resume-${uid}`);
        const destPath = path.join(outDir, `${baseName}.pdf`);

        const result = await httpDownload(downloadUrl, destPath, {
            cookies: cookieHeader,
            headers: { Referer: `https://${DOMAIN}/`, Accept: 'application/pdf,application/octet-stream,*/*' },
            timeout: 30000,
        });
        if (!result.success) {
            throw new CommandExecutionError(`附件简历下载失败: ${result.error || '未知错误'}`);
        }

        // 校验确实是 PDF
        const fd = await fs.promises.open(destPath, 'r');
        const buf = Buffer.alloc(5);
        await fd.read(buf, 0, 5, 0);
        await fd.close();
        if (buf.toString('latin1') !== '%PDF-') {
            await fs.promises.rm(destPath, { force: true });
            throw new CommandExecutionError('下载内容不是 PDF（可能是错误页或权限不足）');
        }

        return [{
            uid, status: 'downloaded', name,
            file: destPath, size: result.size, authority_id: authorityId,
            detail: `已下载 ${(result.size / 1024).toFixed(0)}KB`,
        }];
    },
});
