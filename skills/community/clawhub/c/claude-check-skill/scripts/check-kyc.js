/* 可在已登录 claude.ai 页面执行；只返回脱敏状态，不返回组织标识。 */
async function checkKyc() {
  if (location.origin !== 'https://claude.ai') return {error: 'wrong_origin'};
  async function get(path) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 8000);
    try {
      const response = await fetch('https://claude.ai' + path, {
        method: 'GET', credentials: 'same-origin', cache: 'no-store',
        redirect: 'error', signal: controller.signal
      });
      if (!response.ok) throw new Error('http_' + response.status);
      try { return await response.json(); }
      catch (_) { throw new Error(controller.signal.aborted ? 'timeout' : 'invalid_json'); }
    } catch (error) {
      if (controller.signal.aborted) throw new Error('timeout');
      if (/^(http_\d{3}|invalid_json)$/.test(error.message)) throw error;
      throw new Error('network_or_redirect');
    } finally { clearTimeout(timer); }
  }
  const known = new Set(['not_required', 'pending', 'approved', 'denied']);
  try {
    const orgs = await get('/api/organizations');
    if (!Array.isArray(orgs)) return {error: 'invalid_organizations'};
    if (!orgs.length) return {error: 'no_organizations'};
    if (orgs.length > 10) return {error: 'too_many_organizations'};
    const rows = [];
    const started = Date.now();
    for (const [index, org] of orgs.entries()) {
      const row = {organization: index + 1};
      if (Date.now() - started > 25000) {
        rows.push({...row, error: 'time_budget'});
        continue;
      }
      if (typeof org?.uuid !== 'string' || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(org.uuid)) {
        rows.push({...row, error: 'invalid_organization'});
        continue;
      }
      try {
        const data = await get('/api/organizations/' + encodeURIComponent(org.uuid) + '/kyc_status');
        rows.push({...row, status: known.has(data?.status) ? data.status : 'unknown'});
      } catch (error) {
        rows.push({...row, error: error.message});
        if (['http_401', 'http_403', 'http_429'].includes(error.message)) {
          return {rows, incomplete: true, stopped: error.message, checkedAt: new Date().toISOString()};
        }
      }
    }
    return {rows, checkedAt: new Date().toISOString(), scope: 'session_organizations_not_selected_organization'};
  } catch (error) { return {error: error.message}; }
}
