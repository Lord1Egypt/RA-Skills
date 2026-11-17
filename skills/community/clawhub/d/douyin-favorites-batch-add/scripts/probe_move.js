(async () => {
  // 用法：在抖音页面 console 里先设好 window.PROBE_ID / PROBE_FID / PROBE_FNAME 再运行，
  // 或在 eval 前注入：window.PROBE_ID='<作品ID>'; window.PROBE_FID='<收藏夹ID>'; window.PROBE_FNAME='<夹名>'
  const id = window.PROBE_ID || '<作品ID>';
  const fid = window.PROBE_FID || '<收藏夹ID>';
  const fname = window.PROBE_FNAME || '<收藏夹名>';
  const basic = () => {
    const p = new URLSearchParams({device_platform:'webapp',aid:'6383',channel:'channel_pc_web',version_code:'290100',version_name:'29.1.0',update_version_code:'170400',cookie_enabled:'true',platform:'PC',pc_client_type:'1'});
    const m = document.cookie.match(/(?:^|;\s*)msToken=([^;]+)/); if (m) p.set('msToken', decodeURIComponent(m[1]));
    return p;
  };
  const post = async (path, body) => {
    const r = await fetch('https://www.douyin.com' + path + '?' + basic(), {
      method: 'POST', credentials: 'include', cache: 'no-store',
      headers: {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', accept: 'application/json, text/plain, */*'},
      body: new URLSearchParams(body).toString()
    });
    const t = await r.text();
    let j = null; try { j = JSON.parse(t); } catch (e) {}
    return { http: r.status, code: j && j.status_code, msg: j && j.status_msg, raw: t.slice(0, 160) };
  };
  const variants = {
    A: {aweme_id:id, to_collects_id:fid, collects_name:fname, item_type:'2', update_collects_sort:'true'},
    B: {aweme_id:id, item_ids:id, item_type:'2', to_collects_id:fid, collects_name:fname},
    C: {item_ids: JSON.stringify([id]), item_type:'2', to_collects_id:fid, collects_name:fname},
    D: {aweme_id:id, collects_id:fid, collects_name:fname, item_type:'2'},
    E: {aweme_id:id, to_collects_id:fid, item_type:'0', collects_name:fname},
    F: {aweme_id:id, aweme_type:'0', to_collects_id:fid, collects_name:fname, item_type:'2', update_collects_sort:'true'},
    G: {aweme_id:id, to_collects_id:fid, collects_name:fname, item_type:'2', update_collects_sort:'true', item_ids:JSON.stringify([id])}
  };
  const out = {};
  for (const [k, v] of Object.entries(variants)) {
    out[k] = await post('/aweme/v1/web/collects/video/move/', v);
    await new Promise(r => setTimeout(r, 900));
  }
  return JSON.stringify(out);
})()
