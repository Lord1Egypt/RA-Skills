/**
 * GEO违禁词检测 - License Key 验证服务
 * 
 * 部署到 Cloudflare Workers（免费，每天10万次请求）
 * 需要：创建 KV namespace "KEYS" 并绑定到 Worker
 * 环境变量：ADMIN_TOKEN（管理令牌，用于发Key/查余额）
 * 
 * API 接口：
 *   POST /verify        - 验证Key并扣减1次（用户脚本调用）
 *   POST /admin/add     - 添加/充值Key（管理员调用）
 *   GET  /admin/balance - 查询Key余额（管理员调用）
 *   POST /admin/revoke  - 吊销Key（管理员调用）
 *   GET  /              - 健康检查
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // ---------- POST /verify ----------
      if (path === '/verify' && request.method === 'POST') {
        const body = await request.json();
        const apiKey = body.api_key;

        if (!apiKey) {
          return jsonResp({ valid: false, message: '缺少 api_key 参数' }, 400, corsHeaders);
        }

        const keyData = await env.KEYS.get(`key:${apiKey}`, 'json');

        if (!keyData) {
          return jsonResp({ valid: false, message: 'API Key 无效，请检查或购买' }, 403, corsHeaders);
        }

        if (keyData.credits <= 0) {
          return jsonResp({ valid: false, remaining: 0, message: '额度已用完，请充值' }, 403, corsHeaders);
        }

        // 扣减 1 次
        keyData.credits -= 1;
        keyData.total_used = (keyData.total_used || 0) + 1;
        keyData.last_used = new Date().toISOString();

        await env.KEYS.put(`key:${apiKey}`, JSON.stringify(keyData));

        return jsonResp({
          valid: true,
          remaining: keyData.credits,
          message: '验证成功'
        }, 200, corsHeaders);
      }

      // ---------- POST /admin/add ----------
      if (path === '/admin/add' && request.method === 'POST') {
        const body = await request.json();

        if (body.admin_token !== env.ADMIN_TOKEN) {
          return jsonResp({ error: '管理令牌无效' }, 403, corsHeaders);
        }

        const apiKey = body.api_key || generateKey();
        const credits = body.credits || 100;
        const note = body.note || '';

        // 充值模式：累加额度
        const existing = await env.KEYS.get(`key:${apiKey}`, 'json');
        const totalCredits = existing ? existing.credits + credits : credits;

        const keyData = {
          credits: totalCredits,
          total_used: existing?.total_used || 0,
          created_at: existing?.created_at || new Date().toISOString(),
          last_used: existing?.last_used || null,
          note: note || existing?.note || ''
        };

        await env.KEYS.put(`key:${apiKey}`, JSON.stringify(keyData));

        return jsonResp({
          success: true,
          api_key: apiKey,
          credits: totalCredits,
          message: `Key 已添加/充值成功，当前余额 ${totalCredits} 次`
        }, 200, corsHeaders);
      }

      // ---------- GET /admin/balance ----------
      if (path === '/admin/balance' && request.method === 'GET') {
        const adminToken = url.searchParams.get('admin_token');
        const apiKey = url.searchParams.get('api_key');

        if (adminToken !== env.ADMIN_TOKEN) {
          return jsonResp({ error: '管理令牌无效' }, 403, corsHeaders);
        }

        const keyData = await env.KEYS.get(`key:${apiKey}`, 'json');

        if (!keyData) {
          return jsonResp({ error: 'Key 不存在' }, 404, corsHeaders);
        }

        return jsonResp({
          api_key: apiKey,
          remaining: keyData.credits,
          total_used: keyData.total_used,
          created_at: keyData.created_at,
          last_used: keyData.last_used,
          note: keyData.note
        }, 200, corsHeaders);
      }

      // ---------- POST /admin/revoke ----------
      if (path === '/admin/revoke' && request.method === 'POST') {
        const body = await request.json();

        if (body.admin_token !== env.ADMIN_TOKEN) {
          return jsonResp({ error: '管理令牌无效' }, 403, corsHeaders);
        }

        await env.KEYS.delete(`key:${body.api_key}`);

        return jsonResp({ success: true, message: `Key ${body.api_key} 已吊销` }, 200, corsHeaders);
      }

      // ---------- GET / (健康检查) ----------
      if (path === '/' || path === '') {
        return jsonResp({
          service: 'GEO 违禁词检测 Key 验证服务',
          status: 'running',
          version: '1.0.0',
          endpoints: ['/verify', '/admin/add', '/admin/balance', '/admin/revoke']
        }, 200, corsHeaders);
      }

      return jsonResp({ error: 'Not found' }, 404, corsHeaders);

    } catch (err) {
      return jsonResp({ error: err.message }, 500, corsHeaders);
    }
  }
};

// ---------- 辅助函数 ----------

function jsonResp(data, status, corsHeaders) {
  return new Response(JSON.stringify(data), {
    status: status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders
    }
  });
}

function generateKey() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let key = 'gw-';
  for (let i = 0; i < 24; i++) {
    key += chars[Math.floor(Math.random() * chars.length)];
  }
  return key;
}
