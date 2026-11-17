// claude.ai/share/<uuid>：必须走浏览器。
// 页面 HTML 里没有正文，数据由客户端请求 /api/chat_snapshots/<uuid> 拿到；
// 该接口直连会被 Cloudflare 挑战（403 Just a moment），只有浏览器上下文带得上 cf cookie。
// 所以策略是：用浏览器打开页面过挑战，然后在页面内 fetch 同一个接口拿结构化 JSON，
// 不做 DOM 转换（比 DOM 准确，也不受渲染差异影响）。
import { fmtClock, pickJson } from '../lib/md.mjs';

export const name = 'claude.ai';
export const channel = 'browser';
export const match = (url) => /(^|\/\/|\.)claude\.ai\/share\//.test(url);


export async function read(url, { session, keepOpen = false } = {}) {
  const uuid = (url.match(/\/share\/([0-9a-f-]{36})/i) || [])[1];
  if (!uuid) throw new Error('URL 里没有 share id（应为 36 位 UUID）');

  if (!session) throw new Error('这个站点需要浏览器后端，但调用方没有传入 session');
  await session.open(url);
  try {
    // 等 SPA 渲染出正文；Cloudflare 挑战通常 10 到 20 秒
    await session.waitReady({ minText: 300, tries: 12, delay: 3000 });

    const code = `
      fetch("/api/chat_snapshots/${uuid}?rendering_mode=messages&render_all_tools=true",
            { headers: { "accept": "application/json" } })
        .then(r => r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status)))
        .then(j => JSON.stringify({
          name: j.snapshot_name || "",
          created: j.created_at || null,
          msgs: (j.chat_messages || []).map(m => ({
            sender: m.sender,
            time: m.created_at,
            parts: (m.content || []).filter(c => c.type === "text" && c.text).map(c => c.text)
          }))
        }))
        .catch(e => JSON.stringify({ error: String(e) }))
    `;

    const raw = await session.eval(code);
    const data = pickJson(raw);
    if (data.error) throw new Error('页面内取快照失败：' + data.error);

    const messages = [];
    for (const m of data.msgs || []) {
      const body = (m.parts || []).join('\n\n');
      if (!body.trim()) continue;
      messages.push({
        role: m.sender === 'human' ? '用户' : 'Claude',
        time: fmtClock(m.time),
        body,
      });
    }

    return {
      title: data.name || 'Claude 分享',
      messages,
      source: `https://claude.ai/api/chat_snapshots/${uuid}`,
      note: '分享快照，可能不包含附件与工具调用原始数据',
    };
  } finally {
    if (!keepOpen) await session.close();
  }
}
