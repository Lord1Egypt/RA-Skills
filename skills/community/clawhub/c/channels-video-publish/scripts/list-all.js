// 拉取视频号已发布/待发布全量列表（puppeteer-core 直连 CDP）
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const OUT = '/Users/jx/Downloads/.workbuddy/macros/ch-posts.json';

(async () => {
  const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222', defaultViewport: null });
  const pages = await browser.pages();
  let page = pages.find(p => p.url().includes('channels.weixin.qq.com'));
  if (!page) {
    page = await browser.newPage();
    await page.goto('https://channels.weixin.qq.com/platform/post/list', { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  await new Promise(r => setTimeout(r, 8000));

  // 找一个能看到 mmfinderassistant 域的 frame（新 UI 表单在 iframe 里）
  const frames = page.frames();
  console.log('frames:', frames.length);
  const cand = frames.filter(f => {
    try { return f.url().includes('channels.weixin.qq.com'); } catch (e) { return false; }
  });
  console.log('候选 frame:', cand.map(f => f.url().slice(0, 90)).join('\n  '));

  const doFetch = async (frame) => {
    return await frame.evaluate(async () => {
      const url = '/cgi-bin/mmfinderassistant-bin/post/post_list?_aid=61fff738-15e6-484f-9fcf-249372138f19&_pageUrl=' +
        encodeURIComponent('https://channels.weixin.qq.com/micro/content/post/list');
      const base = {
        pageSize: 100, currentPage: 1, userpageType: 11, stickyOrder: true,
        timestamp: String(Date.now()), _log_finder_uin: '', _log_finder_id: '',
        rawKeyBuff: '', pluginSessionId: null, scene: 7, reqScene: 7,
      };
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(base),
      });
      const j = await r.json();
      return { errCode: j.errCode, errMsg: j.errMsg, data: j.data };
    });
  };

  let res = null;
  for (const f of cand) {
    try {
      const r = await doFetch(f);
      if (r && r.data && Array.isArray(r.data.list) && r.data.list.length) { res = r; break; }
      if (r && r.errCode) console.log('  frame', f.url().slice(0, 60), 'errCode', r.errCode, r.errMsg || '');
    } catch (e) {
      console.log('  frame 失败:', f.url().slice(0, 60), e.message.slice(0, 80));
    }
  }
  if (!res) {
    // 兜底：主框架再试一次
    try { res = await doFetch(page.mainFrame()); } catch (e) { console.log('mainFrame 失败', e.message); }
  }
  if (!res || !res.data || !res.data.list) {
    console.log('❌ 未拿到列表，可能需要重新登录。原始响应:', JSON.stringify(res).slice(0, 400));
    await browser.disconnect();
    process.exit(3);
  }

  const list = res.data.list;
  console.log('errCode:', res.errCode, 'total:', res.data.total, '返回条数:', list.length);
  console.log('\n--- 第一条完整字段（用于确认字段名）---');
  console.log(Object.keys(list[0]).join(', '));

  const parseDesc = (d) => {
    let s = '';
    try {
      if (typeof d === 'string') { const o = JSON.parse(d); s = o.description || o.desc || ''; }
      else if (d && typeof d === 'object') s = d.description || '';
    } catch (e) { s = String(d || '').slice(0, 80); }
    return (s || '').replace(/\s+/g, ' ').trim();
  };

  const fmt = (t) => t ? new Date(t * 1000).toISOString().replace('T', ' ').slice(0, 16) : '-';
  const items = list.map((it, i) => ({
    i,
    desc: parseDesc(it.desc).slice(0, 80),
    createTime: it.createTime,
    effectiveTime: it.effectiveTime,
    createStr: fmt(it.createTime),
    effectStr: fmt(it.effectiveTime),
    isDeclared: it.originalInfo ? it.originalInfo.isDeclared : null,
    status: it.status,
    objectId: it.objectId || it.id || '',
  }));
  fs.writeFileSync(OUT, JSON.stringify(items, null, 2));
  console.log('\n已保存', items.length, '条 ->', OUT);

  // 按发布时间倒序
  items.sort((a, b) => (b.effectiveTime || b.createTime || 0) - (a.effectiveTime || a.createTime || 0));
  console.log('\n=== 全部条目（按时间倒序，前 40 条）===');
  items.slice(0, 40).forEach(it => {
    console.log(`[${it.effectStr}] orig=${it.isDeclared} st=${it.status} | ${it.desc}`);
  });

  await browser.disconnect();
})().catch(e => { console.error('FATAL', e.stack); process.exit(1); });
