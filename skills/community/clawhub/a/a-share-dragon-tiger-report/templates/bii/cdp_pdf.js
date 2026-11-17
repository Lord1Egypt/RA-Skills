// cdp_pdf.js — 通过 CDP 用精确纸张参数导出 PDF（纸张由源 HTML 的 @page 决定）
// 用法: node cdp_pdf.js <cdp-http-endpoint> <out.pdf> [extraWaitMs] [orientation]
//   extraWaitMs 默认 1200。页面含 Chart.js / canvas 图表时，字体就绪不代表图表已绘完，
//   需要额外等待绘制；配合图表配置 animation:false 使用，建议 2000~2500。
//   orientation 默认 'css' —— 完全不干预方向，由源 HTML 的 @page{size:...} 说了算。
//     可用 'landscape' / 'portrait' 显式覆盖。**不要**再硬编码 landscape：
//     同一份导出器要同时服务「A4 横向（BII 双栏）」和「A4 纵向（classic）」两套模板，
//     硬编码方向会把纵向模板导成横向、每页被拦腰截断，而且看起来"只是排版怪"，不易察觉。
const fs = require('fs');

async function main() {
  let cdp = (process.argv[2] || '').trim();
  const out = process.argv[3];
  const orient = (process.argv[5] || 'css').toLowerCase();
  // 兼容 ws://host:port/devtools/browser/xxx 形式：派生出 http 基址
  if (/^wss?:\/\//i.test(cdp)) {
    const u = new URL(cdp);
    cdp = (u.protocol === 'wss:' ? 'https://' : 'http://') + u.host;
  }
  cdp = cdp.replace(/\/+$/, '');
  const list = await (await fetch(cdp + '/json/list')).json();
  const pages = list.filter(t => t.type === 'page');
  if (!pages.length) throw new Error('找不到 page target: ' + JSON.stringify(list));
  // 无头 Chrome 常会额外开一个 about:blank / chrome:// 标签，可能排在列表前面或后面；
  // 优先挑 file:// 页面，否则真的会导出一张空白 PDF（页数还是 1，不易察觉）。
  const filePages = pages.filter(t => /^file:\/\//i.test(t.url));
  const target = (filePages.length ? filePages : pages)[(filePages.length ? filePages : pages).length - 1];
  console.log('target:', target.url);

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  const send = (method, params) => new Promise((res, rej) => {
    const mid = ++id;
    pending.set(mid, { res, rej });
    ws.send(JSON.stringify({ id: mid, method, params: params || {} }));
  });

  ws.addEventListener('message', (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) {
      const { res, rej } = pending.get(m.id);
      pending.delete(m.id);
      m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
    }
  });

  // 静默失败防护：ws 被关闭/出错时明确报出来，避免"exit 0 但文件根本没生成"
  ws.addEventListener('close', () => {
    if (out && !fs.existsSync(out)) console.log('[warn] WebSocket 已关闭，但 PDF 未写出 —— 检查是否撞上消息体积上限');
  });
  ws.addEventListener('error', (e) => console.log('[ws error]', e.message || e.type));

  await new Promise((res, rej) => {
    ws.addEventListener('open', res);
    ws.addEventListener('error', rej);
  });

  // 等待页面字体/布局就绪
  await send('Runtime.evaluate', { expression: 'document.fonts ? document.fonts.ready.then(()=>1) : 1', awaitPromise: true });

  // 额外等待：canvas 图表（Chart.js 等）是异步绘制的，字体就绪不等于图表已出图
  const extraWait = Number(process.argv[4] || 1200);
  const nCanvas = await send('Runtime.evaluate', {
    expression: 'document.querySelectorAll("canvas").length', returnByValue: true,
  }).then(r => r?.result?.value ?? 0).catch(() => 0);
  if (nCanvas > 0) console.log('检测到', nCanvas, '个 canvas，等待图表绘制…');
  await new Promise(r => setTimeout(r, extraWait));

  // ── transferMode: 'ReturnAsStream' 是必须的 ──
  // 大 PDF（base64 后 >8MB 左右）走默认的单条消息会撞上 WebSocket 的
  // "Max decompressed message size exceeded"：ws 被浏览器关闭，脚本静默退出、
  // 文件根本不落地，且 exit code 仍是 0，看起来像"命令没跑"。
  // 改用流 + IO.read 分块（每块 256KB），任意体积都能取回。
  const opts = {
    printBackground: true,
    displayHeaderFooter: false,
    preferCSSPageSize: true,   // 让 CSS @page { size: ... } 决定纸张与方向
    marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0,
    transferMode: 'ReturnAsStream',
  };
  if (orient === 'landscape' || orient === 'portrait') {
    // 仅在显式指定时才钉方向；同时给回退纸张尺寸（preferCSSPageSize 生效时被忽略）
    opts.landscape = orient === 'landscape';
    opts.paperWidth = orient === 'landscape' ? 11.6929 : 8.2677;   // A4 横 / 纵 宽
    opts.paperHeight = orient === 'landscape' ? 8.2677 : 11.6929;  // A4 横 / 纵 高
  }
  const r = await send('Page.printToPDF', opts);

  let buf;
  if (r.stream) {
    const chunks = [];
    for (;;) {
      const c = await send('IO.read', { handle: r.stream, size: 262144 });
      chunks.push(Buffer.from(c.data, c.base64Encoded ? 'base64' : 'binary'));
      if (c.eof) break;
    }
    try { await send('IO.close', { handle: r.stream }); } catch (e) { /* ignore */ }
    buf = Buffer.concat(chunks);
  } else {
    buf = Buffer.from(r.data, 'base64');   // 回退：该 Chrome 不支持 ReturnAsStream
  }

  fs.writeFileSync(out, buf);
  console.log('方向:', orient === 'css' ? '由 CSS @page 决定' : orient);
  console.log('PDF 已写出:', out, fs.statSync(out).size, 'bytes');
  ws.close();
}

main().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
