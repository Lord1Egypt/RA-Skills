// chatgpt.com/share/<id>：纯 HTTP。
// 公开后端接口 backend-api/share/<id> 免认证返回完整 JSON，
// mapping 是节点树，从 current_node 沿 parent 回溯即得主链。
import { httpGetJson } from '../lib/http.mjs';
import { fmtClock } from '../lib/md.mjs';

export const name = 'chatgpt.com';
export const channel = 'http';
export const match = (url) => /(^|\/\/|\.)chatgpt\.com\/share\//.test(url);

export async function read(url) {
  const m = url.match(/\/share\/([0-9a-f-]{36})/i);
  if (!m) throw new Error('URL 里没有 share id（应为 36 位 UUID）');
  const api = `https://chatgpt.com/backend-api/share/${m[1]}`;
  const data = await httpGetJson(api);

  const chain = [];
  let cur = data.current_node;
  const guard = new Set();
  while (cur && data.mapping[cur] && !guard.has(cur)) {
    guard.add(cur);
    chain.push(data.mapping[cur]);
    cur = data.mapping[cur].parent;
  }
  chain.reverse();

  const messages = [];
  for (const node of chain) {
    const msg = node.message;
    if (!msg) continue;
    const role = msg.author && msg.author.role;
    if (role !== 'user' && role !== 'assistant') continue;
    // 隐藏消息是系统注入（如「定制指令不可用」），页面不显示，也不该进文档
    if (msg.metadata && msg.metadata.is_visually_hidden_from_conversation) continue;
    const content = msg.content || {};
    if (content.content_type !== 'text') continue;
    const body = (content.parts || []).filter((p) => typeof p === 'string').join('\n\n');
    if (!body.trim()) continue;
    messages.push({
      role: role === 'user' ? '用户' : 'ChatGPT',
      time: fmtClock(msg.create_time),
      body,
    });
  }

  return { title: data.title || 'ChatGPT 分享', messages, source: api };
}
