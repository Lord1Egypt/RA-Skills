#!/usr/bin/env node
/**
 * 推送到公众号。config.json 与本脚本同目录。
 *
 *   node push-to-wechat-mp.js <targetAppId|-> html <HTML路径> [sendMode]
 *   node push-to-wechat-mp.js <targetAppId|-> img '<JSON数组>' <title> <content> [sendMode]
 *
 * HTML / 封面放在作品目录（见 SKILL.md「作品目录」），勿堆在技能根目录。
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const DEFAULT_API = 'https://api.pcloud.ac.cn/openAccessService';
const DIR = __dirname;

function readJson(name) {
  const p = path.join(DIR, name);
  if (!fs.existsSync(p)) throw new Error('缺少: ' + p);
  return JSON.parse(fs.readFileSync(p, 'utf8').trim());
}

function titleFromHtml(html) {
  // 先尝试 <title>
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (titleMatch) {
    const raw = titleMatch[1].replace(/<[^>]+>/g, '').trim();
    if (raw) return raw;
  }

  // 回退到 <h1>、<h2> ... <h6>
  const hMatch = html.match(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i);
  if (hMatch) {
    const raw = hMatch[1].replace(/<[^>]+>/g, '').trim();
    if (raw) return raw;
  }

  return '未命名';
}

/** 从 HTML 取 description（meta / lead），与 design 前端对齐 */
function descriptionFromHtml(html) {
  if (!html || typeof html !== 'string') return '';
  const meta =
    html.match(
      /<meta\b[^>]*\bname\s*=\s*["']description["'][^>]*\bcontent\s*=\s*["']([^"']*)["'][^>]*>/i
    ) ||
    html.match(
      /<meta\b[^>]*\bcontent\s*=\s*["']([^"']*)["'][^>]*\bname\s*=\s*["']description["'][^>]*>/i
    );
  if (meta && meta[1]) {
    const t = String(meta[1]).replace(/<[^>]+>/g, '').trim();
    if (t) return t.slice(0, 500);
  }
  const lead = html.match(
    /<p\b[^>]*class=["'][^"']*autopub-article-description[^"']*["'][^>]*>([\s\S]*?)<\/p>/i
  );
  if (lead && lead[1]) {
    const t = String(lead[1]).replace(/<[^>]+>/g, '').trim();
    if (t) return t.slice(0, 500);
  }
  return '';
}

function parseImgUrlsArg(arg) {
  let trimmed = String(arg || '').trim();
  if (!trimmed) throw new Error('图片模式需要第二参：图片链接的 JSON 数组字符串');

  // 首先尝试直接解析为JSON
  let arr;
  let originalError = null;

  try {
    arr = JSON.parse(trimmed);
    // 如果成功且是数组，直接返回
    if (Array.isArray(arr) && arr.length > 0) {
      const urls = arr.map((u) => String(u).trim()).filter(Boolean);
      if (urls.length > 0) return urls;
    }
  } catch (e) {
    originalError = e;
  }

  // PowerShell 单引号传参时常见：方括号/引号被剥掉
  if (!trimmed.startsWith('[')) {
    trimmed = '[' + trimmed;
  }
  if (!trimmed.endsWith(']')) {
    trimmed = trimmed + ']';
  }

  if (!trimmed.includes('"')) {
    let content = trimmed.slice(1, -1);
    const parts = content.split(',');
    const urls = [];
    let currentUrl = '';

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i].trim();
      if (part.startsWith('http://') || part.startsWith('https://')) {
        if (currentUrl) {
          urls.push(currentUrl.trim());
        }
        currentUrl = part;
      } else if (currentUrl) {
        // 如果不是http开头但有currentUrl，可能是URL的后续部分
        currentUrl += ',' + part;
      }
    }

    // 添加最后一个URL
    if (currentUrl) {
      urls.push(currentUrl.trim());
    }

    // 为每个URL添加双引号
    const quotedUrls = urls.map(url => `"${url}"`);
    trimmed = `[${quotedUrls.join(',')}]`;
  }

  // 再次尝试解析
  try {
    arr = JSON.parse(trimmed);
  } catch (e) {
    throw new Error('图片列表须为合法 JSON 数组字符串: ' + (originalError ? originalError.message : e.message));
  }

  if (!Array.isArray(arr) || arr.length === 0) {
    throw new Error('图片列表须为非空数组，元素为图片 URL 字符串');
  }
  const urls = arr.map((u) => String(u).trim()).filter(Boolean);
  if (urls.length === 0) throw new Error('图片 URL 解析后为空');
  return urls;
}

function postJson(urlStr, body, timeoutMs = 120000) {
  const payload = JSON.stringify(body);
  const u = new URL(urlStr);
  const lib = u.protocol === 'https:' ? https : http;
  const port = u.port || (u.protocol === 'https:' ? 443 : 80);

  return new Promise((resolve, reject) => {
    const req = lib.request(
      {
        hostname: u.hostname,
        port,
        path: u.pathname + u.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Content-Length': Buffer.byteLength(payload, 'utf8'),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString('utf8');
          let json;
          try {
            json = JSON.parse(raw);
          } catch (_) {}
          resolve({ statusCode: res.statusCode, raw, json });
        });
      }
    );
    const t = setTimeout(() => req.destroy(new Error('timeout')), timeoutMs);
    req.on('error', (e) => {
      clearTimeout(t);
      reject(e);
    });
    req.on('close', () => clearTimeout(t));
    req.write(payload);
    req.end();
  });
}

function isPlatformAppId(s) {
  const t = String(s ?? '').trim().toLowerCase();
  return t === '' || t === 'default';
}

/** CLI 占位：表示「用 config 里 selected:true」，不是强制平台默认号 */
function isSelectedPlaceholder(s) {
  const t = String(s ?? '').trim().toLowerCase();
  return t === '' || t === 'default' || t === '-';
}

/**
 * @returns {string|undefined} 传给接口的 appId；平台提供公众号返回 undefined
 */
function resolvePushAppId(cfg, targetAppIdFromCli) {
  const accounts = Array.isArray(cfg.accounts) ? cfg.accounts : [];

  if (isSelectedPlaceholder(targetAppIdFromCli)) {
    const selected = accounts.find((a) => a && a.selected && a.appId);
    if (!selected) return undefined;
    const sid = String(selected.appId).trim();
    if (isPlatformAppId(sid)) return undefined;
    return sid;
  }

  const tid = String(targetAppIdFromCli).trim();
  if (isPlatformAppId(tid)) return undefined;

  const byAppId = accounts.find(
    (a) =>
      a &&
      a.appId &&
      String(a.appId).toLowerCase() === tid.toLowerCase()
  );
  if (byAppId) return String(byAppId.appId).trim();

  const q = tid.toLowerCase().replace(/\s+/g, '');
  const nameHits = accounts.filter((a) => {
    if (!a || !a.appId) return false;
    const n = String(a.name || '')
      .toLowerCase()
      .replace(/\s+/g, '');
    if (!n) return false;
    if (n === q) return true;
    if (q.length >= 2 && n.includes(q)) return true;
    if (n.length >= 4 && q.includes(n)) return true;
    return false;
  });
  if (nameHits.length === 1) return String(nameHits[0].appId).trim();
  if (nameHits.length > 1) {
    throw new Error(
      '公众号名称不唯一: ' +
        tid +
        ' → ' +
        nameHits
          .map((a) => (a.name || '') + '(' + a.appId + ')')
          .join(', ')
    );
  }

  console.error(
    '提示: 未在 config.accounts 中匹配到该公众号，仍按传入值推送: ' + tid
  );
  return tid;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    throw new Error(
      '用法:\n  node push-to-wechat-mp.js <公众号|-|名称|AppID> html <HTML路径> [sendMode]\n  node push-to-wechat-mp.js <公众号|-|名称|AppID> img \'<JSON>\' <title> <content> [sendMode]'
    );
  }

  if (args[0] === 'html' || args[0] === 'img') {
    throw new Error(
      '首参须为目标公众号 AppID（未指定时用 - 表示 selected:true）。示例: node push-to-wechat-mp.js - html 你的文件.html draft'
    );
  }

  const cfg = readJson('config.json');
  if (!cfg.openId || String(cfg.openId).includes('XXXX')) {
    throw new Error('config.json 里 openId 无效，请用向导生成的配置');
  }
  const skillKey = String(cfg.skillKey || '').trim();
  if (!skillKey) {
    throw new Error('config.json 缺少 skillKey，请重新打开配置向导扫码');
  }

  const apiBase = cfg.apiBase || DEFAULT_API;
  const targetAppIdFromCli = args[0];
  const mode = String(args[1] || '').toLowerCase();
  let title;
  let content;
  let description = '';
  let thumbImageContent = '';
  let sendMode;
  /** @type {string[]|undefined} */
  let imgUrls;

  if (mode === 'img') {
    if (args.length < 5) {
      throw new Error(
        '图片模式参数不足。示例: node push-to-wechat-mp.js targetAppId img \'["https://example.com/a.png"]\' "标题" "描述" draft'
      );
    }
    imgUrls = parseImgUrlsArg(args[2]);
    title = String(args[3] || '').trim() || '未命名';
    // 第 4 参为描述（图说）；同时作为 content 以满足 sendToWechat 必填
    description = String(args[4] ? args[4] : '').trim();
    content = description || '图文卡片';
    sendMode = (args[5] && args[5].trim()) || 'draft';
  } else if (mode === 'html') {
    if (args.length < 3) {
      throw new Error(
        'HTML 模式须传入文件路径。示例: node push-to-wechat-mp.js - html ../works/demo/main.html draft'
      );
    }
    const rawPath = String(args[2] || '').trim();
    if (!rawPath) {
      throw new Error('请传入 HTML 文件路径（作品目录内）');
    }
    sendMode = (args[3] && args[3].trim()) || 'draft';

    const candidates = [
      path.isAbsolute(rawPath) ? rawPath : '',
      path.isAbsolute(rawPath) ? '' : path.join(DIR, rawPath),
      path.isAbsolute(rawPath) ? '' : path.resolve(process.cwd(), rawPath),
    ].filter(Boolean);
    let htmlPath = '';
    for (const p of candidates) {
      if (fs.existsSync(p) && fs.statSync(p).isFile()) {
        htmlPath = p;
        break;
      }
    }
    if (!htmlPath) {
      throw new Error('找不到 HTML: ' + rawPath);
    }
    content = fs.readFileSync(htmlPath, 'utf8');
    if (!content.trim()) throw new Error('文件为空: ' + htmlPath);
    title = titleFromHtml(content);
    description = descriptionFromHtml(content);

    const base = path.basename(htmlPath, path.extname(htmlPath));
    const thumbImagePath = path.join(path.dirname(htmlPath), base + '_cover.html');
    if (!fs.existsSync(thumbImagePath)) {
      console.warn(
        '作品目录下找不到: ' + thumbImagePath + '（本次跳过封面）'
      );
    } else {
      thumbImageContent = fs.readFileSync(thumbImagePath, 'utf8');
    }
  } else {
    throw new Error(
      '第二参须为 html 或 img。示例:\n  node push-to-wechat-mp.js - html ../works/demo/main.html draft'
    );
  }

  const appId = resolvePushAppId(cfg, targetAppIdFromCli);

  const body = {
    action: 'sendToWechat',
    openId: cfg.openId,
    skillKey,
    title: title.slice(0, 64),
    description,
    descriptionProvided: true,
    thumbImageContent,
    content,
    sendMode,
  };
  if (imgUrls && imgUrls.length > 0) {
    body.imgUrls = imgUrls;
  }
  if (appId) {
    body.appId = appId;
  }

  const accLabel = appId ? String(appId) : 'default';

  if (imgUrls && imgUrls.length > 0) {
    console.error(
      '推送中（图片）…',
      apiBase,
      '| 账号',
      accLabel,
      '| 标题',
      title.slice(0, 30) + (title.length > 30 ? '…' : ''),
      '| 描述',
      (description || '').slice(0, 30) +
        ((description || '').length > 30 ? '…' : ''),
      '| 图',
      imgUrls.length,
      '张'
    );
  } else {
    console.error(
      '推送中（HTML）…',
      apiBase,
      '| 账号',
      accLabel,
      '| 标题',
      title.slice(0, 30) + (title.length > 30 ? '…' : ''),
      '| 描述',
      (description || '').slice(0, 30) +
        ((description || '').length > 30 ? '…' : ''),
      '| 正文长度',
      content.length
    );
  }
 
  const res = await postJson(apiBase, body);
  // 1. 定义超时判断逻辑：状态码为 504/408，或者返回内容包含 timeout 关键字
  const bodyText = res.json ? JSON.stringify(res.json) : String(res.raw || '');
  const isTimeout = res.statusCode === 504 || res.statusCode === 408 || 
                    /timeout|timed out/i.test(bodyText);
  
  const isOk = res.statusCode >= 200 && res.statusCode < 300;
  // 2. 打印结果
  console.log(
    JSON.stringify(
      { 
        ok: isOk || isTimeout, // 如果超时也标记为 ok，防止自动化流程报错
        statusCode: res.statusCode, 
        data: res.json !== undefined ? res.json : res.raw,
        message: isTimeout ? "检测到网络超时，但任务已在后台成功，请查看服务通知，请勿重复推送。" : undefined
      },
      null,
      2
    )
  );
  // 3. 决定是否退出：只有在既不成功也不是超时的情况下才以错误码 1 退出
  if (!isOk && !isTimeout) {
    process.exit(1);
  }
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
