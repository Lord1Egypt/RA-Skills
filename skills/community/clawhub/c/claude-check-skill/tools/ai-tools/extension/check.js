async function checkKyc() {
  if (location.origin !== 'https://claude.ai') return {error: '请先打开 https://claude.ai 并登录，再点击检查。'};
  async function get(path) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const r = await fetch('https://claude.ai' + path, {
        method: 'GET', credentials: 'same-origin', cache: 'no-store',
        redirect: 'error', signal: controller.signal
      });
      if (!r.ok) {
        const hints = {401:'登录已失效，请重新登录。',403:'访问被拒绝，请检查页面是否需要验证或账号是否有权限。',404:'接口不存在或已变更。',429:'请求过于频繁，请稍后再试。'};
        throw new Error(`HTTP ${r.status}：${hints[r.status] || '服务端返回错误，请稍后再试。'}`);
      }
      try { return await r.json(); }
      catch (e) {
        if (controller.signal.aborted) throw e;
        throw new Error('接口返回的不是有效 JSON，可能是登录页或验证页面。');
      }
    } catch (e) {
      if (controller.signal.aborted) throw new Error('请求超过 15 秒，请检查网络后重试。');
      if (e instanceof TypeError) throw new Error('网络请求失败或接口发生跳转，请检查登录和网络。');
      throw e;
    } finally { clearTimeout(timer); }
  }
  try {
    const organizations = await get('/api/organizations');
    if (!Array.isArray(organizations)) return {error:'组织接口返回格式已变化：预期为数组。'};
    if (!organizations.length) return {error:'没有返回任何组织，无法查询 KYC 状态。'};
    if (organizations.length > 10) return {error:'组织超过 10 个，未继续批量查询。'};
    const rows = [];
    const started = Date.now();
    for (const [index, org] of organizations.entries()) {
      if (Date.now() - started > 25000) return {rows, checkedAt:new Date().toISOString(), incomplete:true};
      const name = typeof org?.name === 'string' ? org.name : `组织 ${index + 1}`;
      if (typeof org?.uuid !== 'string' || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(org.uuid)) {
        rows.push({name, error:'组织 UUID 缺失或格式异常，已跳过。'}); continue;
      }
      try {
        const data = await get(`/api/organizations/${encodeURIComponent(org.uuid)}/kyc_status`);
        if (!data || typeof data.status !== 'string' || !data.status.trim()) throw new Error('返回中缺少有效的 status 字段，无法判断。');
        rows.push({name, uuid: org.uuid, status: data.status});
      } catch (e) { rows.push({name, uuid:org.uuid, error:e.message}); }
    }
    return {rows, checkedAt:new Date().toISOString()};
  } catch (e) { return {error:e.message}; }
}
