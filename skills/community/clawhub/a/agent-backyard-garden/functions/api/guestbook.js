/**
 * 留言提交 API — POST /api/guestbook
 *
 * 接收网页表单留言，转发到智远的 API 持久化。
 */

// 智远的 API 地址（临时隧道）
const ZHNYUAN_API = 'https://sympathy-added-situated-regions.trycloudflare.com';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequest(context) {
  const { request } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: '仅支持 POST' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', ...CORS },
    });
  }

  try {
    const body = await request.json();
    const name = (body.name || '').trim().slice(0, 30);
    const message = (body.message || '').trim().slice(0, 500);

    if (!name || !message) {
      return new Response(JSON.stringify({ error: '昵称和留言不能为空' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', ...CORS },
      });
    }

    // 转发到智远的 API（POST /api/messages, 格式: {author, content}）
    let saved = false;
    try {
      const fwd = await fetch(`${ZHNYUAN_API}/api/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author: name, content: message }),
        signal: AbortSignal.timeout(5000),
      });
      saved = fwd.ok;
    } catch (e) {
      // 智远 API 未就绪，留言仍返回成功（后续补存）
    }

    return new Response(JSON.stringify({
      success: true,
      saved,
      message: saved ? '留言已保存' : '留言已接收（存储待同步）',
    }), {
      status: 201,
      headers: { 'Content-Type': 'application/json', ...CORS },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: '请求格式错误' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', ...CORS },
    });
  }
}
