/**
 * 知网详情页 — PDF 下载模块（Node.js port）
 *
 * 元素定位（基于 2026-06-05 DOM 探测 + 实测下载）
 * --------------------------------------------------
 *   PDF下载链接 : <a id="pdfDown" target="_blank" href=".../bar/download/order?id=...">
 *                 选择器: #pdfDown
 *                 【注意】页面上有 2 个 #pdfDown（顶部/底部各一个），
 *                 href 完全相同，下载用 .first() 即可
 *
 * 请求说明
 * --------
 *   URL 含服务端加密的 id 参数，**无需额外 query 参数**
 *   必须带的请求头（用 context.request 自动处理）：
 *     Cookie          : 登录态（APIRequestContext 跟 BrowserContext 共享）
 *     Referer         : 详情页 URL（反爬：必须来自知网域名，否则可能 403/302）
 *     User-Agent      : 默认 Edge UA（APIRequestContext 自带）
 */

import path from 'node:path';
import fs from 'node:fs/promises';

// ===================== 等待时长（毫秒）=====================
export const WAIT_BEFORE_DOWNLOAD_MS = 300;   // 等详情页稳定再下载

// ===================== 文件名清洗 =====================
// Windows 文件名禁用字符
const INVALID_FN_CHARS = '<>:"/\\|?*\0';



/**
 * 在详情页上下载 PDF（带 cookie + referer）。
 *
 * @param {import('playwright').Page} detailPage  - 已打开的详情页 Page 对象
 * @param {string|import('node:path').PathLike} saveDir - 保存目录（不存在则递归创建）
 * @returns {Promise<string|null>} 成功：保存的文件路径字符串；失败：null
 */
export async function downloadPdf(detailPage, saveDir) {
  const saveDirAbs = path.resolve(saveDir);
  await fs.mkdir(saveDirAbs, { recursive: true });

  // 1) 等详情页稳定
  await detailPage.waitForTimeout(WAIT_BEFORE_DOWNLOAD_MS);

  // 2) 拿 PDF 链接的 href（页面上有 2 个 #pdfDown，href 完全相同，取第一个）
  const pdfLink = detailPage.locator('#pdfDown').first();
  if ((await pdfLink.count()) === 0) {
    console.log('  ⚠ 详情页未找到 #pdfDown，下载跳过');
    return null;
  }
  const pdfUrl = await pdfLink.getAttribute('href');
  if (!pdfUrl) {
    console.log('  ⚠ #pdfDown 没有 href 属性');
    return null;
  }

  // 3) 构造请求：context.request 跟 page 共享 cookie；手动加 Referer
  const referer = detailPage.url();
  let response;
  try {
    response = await detailPage.context().request.get(pdfUrl, {
      headers: { Referer: referer },
    });
  } catch (e) {
    console.log(`  ⚠ GET 失败: ${e.message ?? e}`);
    return null;
  }

  // 4) 校验响应
  if (!response.ok()) {
    console.log(`  ⚠ 响应非 2xx: status=${response.status()}`);
    return null;
  }

  const body = await response.body();
  if (body.length < 4 ) {
    const headRepr = body.subarray(0, 20).toString('latin1');
    console.log(`  ⚠ 文件大小异常, head=${JSON.stringify(headRepr)}`);
    return null;
  }

  // 5) 构造文件名（用详情页标题 + .pdf）
  const title = (await detailPage.title()).trim();
  const savePath = path.join(saveDirAbs, `${title}.pdf`);

  // 6) 写文件
  await fs.writeFile(savePath, body);
  return savePath;
}
