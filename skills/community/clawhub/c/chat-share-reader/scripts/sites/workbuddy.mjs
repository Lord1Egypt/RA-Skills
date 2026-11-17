// workbuddy.link 分享页：纯 HTTP。
// 外层页面 HTML 内嵌 window.__PUBLISH_BOOTSTRAP__，里面的 artifacts url 指向静态目录，
// 同目录下有 conversation-data.json，content[].text 就是模型输出的 markdown 原文。
import { httpGet, httpGetJson, sliceJsonObject } from '../lib/http.mjs';
import { fmtClock } from '../lib/md.mjs';

export const name = 'workbuddy.link';
export const channel = 'http';
export const match = (url) => /(^|\/\/|\.)workbuddy\.link\/p\//.test(url);

export async function read(url) {
  const html = await httpGet(url);

  let base = null;
  const marker = html.indexOf('__PUBLISH_BOOTSTRAP__');
  if (marker >= 0) {
    const brace = html.indexOf('{', marker);
    const slice = sliceJsonObject(html, brace);
    if (slice) {
      try {
        const boot = JSON.parse(slice);
        base = boot.artifact && boot.artifact.url;
      } catch {
        /* 退回正则 */
      }
    }
  }
  if (!base) {
    const m = html.match(/"url"\s*:\s*"(https:\/\/workbuddy-space-static[^"]+\/)"/);
    if (!m) throw new Error('页面里没找到 artifacts url，格式可能改版了');
    base = m[1];
  }

  const dataUrl = base + 'conversation-data.json';
  const data = await httpGetJson(dataUrl);

  const messages = [];
  for (const msg of data.messages || []) {
    const role = msg.messageType === 'user' ? '用户' : data.assistantName || '助手';
    const parts = (msg.content || []).filter((c) => c.type === 'text' && c.text);
    const body = parts.map((c) => c.text).join('\n\n');
    if (!body.trim()) continue;
    messages.push({ role, time: fmtClock(msg.createTime), body });
  }

  return {
    title: data.name || 'WorkBuddy 分享',
    messages,
    source: dataUrl,
    note: '内容由 AI 生成，请核实重要信息',
  };
}
