// Cloudflare Worker for CryptoFolio
// 部署到 Cloudflare Workers 作为数据存储后端

const TOKEN = 'your-secret-token'; // ⚠️ 修改为你的密码

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const auth = request.headers.get('Authorization');

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Health check (无需认证)
    if (url.pathname === '/api/health') {
      return Response.json({ ok: true, timestamp: Date.now() }, { headers: corsHeaders });
    }

    // 认证检查
    if (auth !== `Bearer ${TOKEN}`) {
      return Response.json(
        { ok: false, error: 'Unauthorized' },
        { status: 401, headers: corsHeaders }
      );
    }

    // GET /api/data - 获取数据
    if (url.pathname === '/api/data' && request.method === 'GET') {
      try {
        const data = await env.KV.get('cryptofolio_data', 'json');
        const defaultData = {
          accounts: [
            { id: 'a1', name: 'Binance', type: 'CEX', color: '#F0B90B' },
            { id: 'a2', name: 'OKX', type: 'CEX', color: '#2563EB' },
            { id: 'a3', name: 'MetaMask', type: 'WALLET', color: '#E97B2E' },
          ],
          positions: [],
          trades: [],
          finance: [],
          transfers: [],
        };
        return Response.json(
          { ok: true, data: data || defaultData },
          { headers: corsHeaders }
        );
      } catch (e) {
        return Response.json(
          { ok: false, error: e.message },
          { status: 500, headers: corsHeaders }
        );
      }
    }

    // POST /api/data - 保存数据
    if (url.pathname === '/api/data' && request.method === 'POST') {
      try {
        const data = await request.json();
        await env.KV.put('cryptofolio_data', JSON.stringify(data));
        return Response.json({ ok: true }, { headers: corsHeaders });
      } catch (e) {
        return Response.json(
          { ok: false, error: e.message },
          { status: 500, headers: corsHeaders }
        );
      }
    }

    // 404
    return Response.json(
      { ok: false, error: 'Not found' },
      { status: 404, headers: corsHeaders }
    );
  },
};
