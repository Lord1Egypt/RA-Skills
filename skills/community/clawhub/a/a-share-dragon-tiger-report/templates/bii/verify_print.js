// vcheck.js — 在「A4 横向打印尺寸」下测量页面高度与图表墨量
// 用法: node vcheck.js <cdp> [printWidthPx=1123] [printHeightPx=794] [urlSubstr]
//
// ⚠️ 两个宽度别搞混：
//   · 纸张宽 297mm ≈ 1123px —— 全出血方案下 .page 的实际宽度（@page margin:0）
//   · 版心宽 273mm ≈ 1032px —— .page 减去左右 12mm padding 后的内容宽度
//   视口必须钉在**【纸张宽 1123】**，SVG/表格才会按打印时的真实尺寸排版；
//   而"是否溢出"要看 .page 的实际高度有没有超过 210mm ≈ 794px。
// 旧版（@page 带 margin）钉的是 1032——若改回 margin 方案，两个值都要同步换。
// canvas id 自动从 DOM 发现（兼容 BII 双栏与 classic 单栏两套模板）
const IDS_FALLBACK = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'];

async function main() {
  let cdp = (process.argv[2] || '').trim();
  const PW = Number(process.argv[3] || 1123);   // A4 横向纸张宽 297mm ≈ 1123px
  const PH = Number(process.argv[4] || 794);    // A4 横向纸张高 210mm ≈ 794px
  if (/^wss?:\/\//i.test(cdp)) { cdp = 'http://' + new URL(cdp).host; }
  cdp = cdp.replace(/\/+$/, '');
  const list = await (await fetch(cdp + '/json/list')).json();
  // 可能开着多个标签：优先按 URL 子串（第 5 个参数）筛选，否则优先 file:// 页面
  // ——无头 Chrome 常会额外开一个 about:blank / chrome:// 标签，且可能排在列表末尾，
  // 直接取 list 最后一个会连到空页上（症状：canvas 总数 0、页面列表为空）。
  const want = (process.argv[5] || '').trim();
  const pages = list.filter(t => t.type === 'page');
  let hits = pages;
  if (want) hits = hits.filter(t => decodeURIComponent(t.url).includes(want));
  if (!hits.length) hits = pages.filter(t => /^file:\/\//i.test(t.url));
  if (!hits.length) hits = pages;
  const page = hits[hits.length - 1];
  if (!page) throw new Error('no page target' + (want ? ` matching "${want}"` : ''));
  if (pages.length > 1) {
    console.log('多标签(' + pages.length + ')：选中', decodeURIComponent(page.url).slice(-60));
  }
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0; const pend = new Map();
  const send = (m, p) => new Promise((res, rej) => {
    const i = ++id; pend.set(i, { res, rej });
    ws.send(JSON.stringify({ id: i, method: m, params: p || {} }));
  });
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pend.has(m.id)) {
      const { res, rej } = pend.get(m.id); pend.delete(m.id);
      m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
    }
  });
  await new Promise((r, j) => { ws.addEventListener('open', r); ws.addEventListener('error', j); });
  await send('Runtime.enable');

  // 关键：把视口宽度钉在打印版心宽度，SVG 才会按打印时的尺寸渲染
  await send('Emulation.setDeviceMetricsOverride', {
    width: PW, height: 1400, deviceScaleFactor: 1, mobile: false
  });
  await new Promise(r => setTimeout(r, 600));

  const expr = `(() => {
    const auto=[...document.querySelectorAll('canvas')].map(c=>c.id).filter(Boolean);
    const ids = auto.length ? auto : ${JSON.stringify(IDS_FALLBACK)};
    const charts = ids.map(id=>{
      const c=document.getElementById(id);
      if(!c) return {id, exists:false};
      const inst = (window.Chart && Chart.getChart) ? !!Chart.getChart(id) : false;
      let ink=0;
      try{
        const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
        for(let i=0;i<d.length;i+=4){ if(d[i+3]>10 && !(d[i]>250&&d[i+1]>250&&d[i+2]>250)) ink++; }
      }catch(e){ return {id, exists:true, chart:inst, err:String(e)}; }
      return {id, exists:true, chart:inst, w:c.width, h:c.height, ink, ratio:+(ink/(c.width*c.height)).toFixed(4)};
    });
    const pages=[...document.querySelectorAll('.page, .cover')].map((p,i)=>{
      const L=p.querySelector('.colL');
      const svg=p.querySelector('.colR svg');
      return {i:i+1, h:Math.round(p.getBoundingClientRect().height),
              lh:L?Math.round(L.scrollHeight):null,
              svg:svg?Math.round(svg.getBoundingClientRect().height):null,
              svgw:svg?Math.round(svg.getBoundingClientRect().width):null};
    });
    return {charts, pages, canvases:document.querySelectorAll('canvas').length,
            vw: window.innerWidth};
  })()`;
  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
  const v = r.result.value;

  console.log('视口宽:', v.vw, '| 纸张宽(297mm):', PW, '| canvas 总数:', v.canvases);
  console.log('--- Chart.js 图表 ---');
  let bad = 0;
  for (const c of v.charts) {
    const ok = c.exists && c.chart && c.ink > 300;
    if (!ok) bad++;
    console.log(`${ok?'OK  ':'FAIL'} ${c.id.padEnd(4)} chart=${c.chart} ${c.w||''}x${c.h||''} ink=${c.ink} ratio=${c.ratio}${c.err?' ERR='+c.err:''}`);
  }
  console.log('--- 页面高度（打印纸张尺寸下，阈值 = A4 横向 210mm）---');
  let over = 0;
  for (const pg of v.pages) {
    const flag = pg.h > PH ? ` ❌ 溢出 ${pg.h-PH}px` : ' ok';
    if (pg.h > PH) over++;
    console.log(`p${String(pg.i).padStart(2,'0')} 页高=${pg.h} 左栏=${pg.lh} svg=${pg.svg}(${pg.svgw}w)${flag}`);
  }
  console.log(bad === 0 ? '✅ 全部 canvas 图表已绘出' : `❌ ${bad} 个 canvas 图表未绘出`);
  console.log(over === 0 ? `✅ 无页面溢出（阈值 ${PH}px = A4 横向 210mm，视口钉在 ${PW}px = 297mm）` : `❌ ${over} 页溢出`);
  await send('Emulation.clearDeviceMetricsOverride').catch(()=>{});
  ws.close();
  process.exit((bad === 0 && over === 0) ? 0 : 2);
}
main().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
