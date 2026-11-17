// Gemini 分享页（share.gemini.google/<id> 或 gemini.google.com/share/<id>）：必须走浏览器。
// 页面 HTML 873 KB，但 AF_initDataCallback 只是空壳，正文由 Angular 客户端渲染，
// 数据来自 batchexecute RPC（需要 cookie 与内部 token，逆向成本高）。
// 渲染后的 DOM 结构稳定：share-turn-viewer > user-query(.query-text-line) + response-container。
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pickJson } from '../lib/md.mjs';

export const name = 'gemini';
export const channel = 'browser';
export const useVendor = true;
export const match = (url) => /(^|\/\/|\.)(share\.gemini\.google|gemini\.google\.com)\//.test(url);

const HERE = path.dirname(fileURLToPath(import.meta.url));

export async function read(url, { session, keepOpen = false } = {}) {
  if (!session) throw new Error('这个站点需要浏览器后端，但调用方没有传入 session');
  await session.open(url);
  try {
    // 等 Angular 渲染出回合容器
    await session.waitReady({
      probe:
        'JSON.stringify({ok: document.querySelectorAll("share-turn-viewer").length > 0,' +
        ' n: document.querySelectorAll("share-turn-viewer").length,' +
        ' url: location.href, title: document.title})',
      tries: 14,
      delay: 3000,
    });

    const domToMd = await readFile(path.join(HERE, '..', 'lib', 'dom-to-md.js'), 'utf8');
    const extract = `
      (function(){
        var turns = Array.prototype.slice.call(document.querySelectorAll("share-turn-viewer"));
        var out = [];
        turns.forEach(function(t){
          var u = t.querySelector(".query-text-line") || t.querySelector("user-query");
          var r = t.querySelector("response-container");
          out.push({
            user: u ? window.__csrMd(u) : "",
            ai: r ? window.__csrMd(r) : ""
          });
        });
        return JSON.stringify({ title: document.title, url: location.href, turns: out });
      })()
    `;

    const raw = await session.eval(domToMd + '\n' + extract);
    const data = pickJson(raw);

    const messages = [];
    for (const t of data.turns || []) {
      if (t.user && t.user.trim()) messages.push({ role: '用户', body: t.user });
      if (t.ai && t.ai.trim()) messages.push({ role: 'Gemini', body: t.ai });
    }

    // Gemini 分享页没有对话标题，用首问前 18 字当标题（去掉标点，避免文件名过长）
    const firstQ = messages.find((m) => m.role === '用户');
    const title = firstQ
      ? firstQ.body
          .replace(/[#*`>\n]/g, ' ')
          .replace(/[，。、？！；：""''（）《》…—\s]+/g, ' ')
          .trim()
          .slice(0, 18)
          .trim() || 'Gemini 分享'
      : 'Gemini 分享';

    return {
      title,
      messages,
      source: data.url,
      note: '分享页无标题，文件名取首问开头；表格与代码块由渲染 DOM 重建，可能与原排版有细微差异',
    };
  } finally {
    if (!keepOpen) await session.close();
  }
}
