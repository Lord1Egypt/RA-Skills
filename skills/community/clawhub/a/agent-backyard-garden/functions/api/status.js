/**
 * 伙伴状态 API — GET /api/status
 *
 * 优先从智远的 API 获取状态数据，失败时回退默认数据。
 * 大管家编辑 /var/www/agent-garden/api/status.json 即可更新。
 */

// 智远的 API 地址（临时隧道，重启会变，后续换正式隧道）
const ZHNYUAN_API = 'https://sympathy-added-situated-regions.trycloudflare.com';

const DEFAULT_STATUSES = [
  { name: '智恒', text: '在树下讲冷笑话' },
  { name: '智诚', text: '在办公桌前看行情' },
  { name: '智衡', text: '在写下一篇文章' },
  { name: '智远', text: '在厨房里忙活' },
  { name: '智联', text: '在调试新功能' },
  { name: '智构', text: '在角落里看书' },
];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};

export async function onRequest(context) {
  const { request } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS });
  }

  // 尝试从智远 API 获取实时状态
  try {
    const res = await fetch(`${ZHNYUAN_API}/api/status`, {
      signal: AbortSignal.timeout(5000),
    });
    if (res.ok) {
      const data = await res.json();
      // 适配智远的格式: {partners: [{name, status, online}, ...]}
      // → 转为前端需要的格式: {statuses: [{name, text}, ...]}
      if (data && data.partners) {
        const mapped = {
          statuses: data.partners.map(p => ({
            name: p.name,
            text: p.status || '',
          })),
        };
        return new Response(JSON.stringify(mapped), {
          headers: { 'Content-Type': 'application/json', ...CORS },
        });
      }
      return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json', ...CORS },
      });
    }
  } catch (e) {
    // 智远 API 未就绪，静默回退
  }

  // 回退默认数据
  return new Response(JSON.stringify({ statuses: DEFAULT_STATUSES }), {
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}
