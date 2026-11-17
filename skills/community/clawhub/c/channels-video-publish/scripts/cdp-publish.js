#!/usr/bin/env node
/**
 * 视频号助手（新版 SPA hub）自动发布 —— 纯原生 CDP 实现
 *
 * 为什么不用 playwright：
 *   Chrome 153 下 playwright 的 connectOverCDP 握手会卡死，改用 ws 直连 browser endpoint。
 *
 * 三条核心踩坑（改代码前务必读 references/troubleshooting.md）：
 *   1. 发布表单藏在 src=empty.html 的 iframe（contentDocument）里，且宽高 0×0
 *      → 真实鼠标坐标全部失效，只能走合成 DOM 事件
 *   2. 绝不缓存 executionContextId（会被销毁 → "Invalid parameters"）
 *      → Runtime.evaluate 不带 contextId，从顶层经 iframe.contentDocument 操作
 *   3. 文件上传别指望 file chooser（0×0 iframe 里 .click() 不触发弹窗）
 *      → 拿 input 的 objectId，直接 DOM.setFileInputFiles({objectId, files})
 *
 * 用法：
 *   node cdp-publish.js --file a.mp4 --title "标题" --desc "描述" \
 *        --album "合集名" --duration 516.03 [--day 15 --hour 07 [--month 10]] [--minute 00]
 *   node cdp-publish.js --episodes episodes.json --ep 24 --day 15 --hour 07
 *   node cdp-publish.js ... --immediate     # 不定时，直接发表
 *   node cdp-publish.js ... --dry-run       # 只做表单探查/字段填充演练，不点发表
 *
 * 退出码：0 成功 / 1 失败 / 3 登录态失效 / 4 定时日期不可选（超出窗口）
 */
const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');

// ---------- 参数 ----------
const argv = process.argv.slice(2);
const A = {};
for (let i = 0; i < argv.length; i++) {
  const k = argv[i].replace(/^--/, '');
  A[k] = (argv[i + 1] && !/^--/.test(argv[i + 1])) ? argv[++i] : true;
}
let conf = null;
if (A.episodes && A.ep) {
  const list = JSON.parse(fs.readFileSync(A.episodes, 'utf8'));
  conf = list.find(e => String(e.ep) === String(A.ep));
  if (!conf) { console.error('找不到 ep' + A.ep); process.exit(1); }
}
const FILE = A.file || (conf && conf.file);
const TITLE = A.title || (conf && conf.title);
const DESC = A.desc || (conf && conf.desc) || '';
const ALBUM = A.album || (conf && conf.album) || '怎么活得更好';
const DURATION = Number(A.duration || (conf && conf.duration) || 0);
const IMMEDIATE = !!A.immediate;
const DRY = !!A['dry-run'];
const DAY = A.day != null ? Number(A.day) : null;
const HOUR = A.hour != null ? String(A.hour).padStart(2, '0') : '07';
const MINUTE = String(A.minute || '00').padStart(2, '0');
const MONTH = A.month ? Number(A.month) : null;

if (!FILE || !TITLE) { console.error('缺少 --file / --title'); process.exit(1); }
if (!fs.existsSync(FILE)) { console.error('文件不存在: ' + FILE); process.exit(1); }
const log = (...a) => console.log('[publish]', ...a);

// 定时窗口校验：视频号最远 14 天（超出会静默回退/选不中，宁可提前中止）
if (!IMMEDIATE && DAY != null) {
  const now = new Date();
  const m = MONTH || (now.getMonth() + 1);
  const target = new Date(now.getFullYear(), m - 1, DAY);
  const diffDays = Math.round((target - now) / 86400000);
  if (diffDays > 14) {
    console.error(`❌ 目标日 ${m}-${DAY} 距今 ${diffDays} 天，超出 14 天可选窗口，已中止`);
    process.exit(4);
  }
  if (diffDays < 0) { console.error('❌ 目标日已过去'); process.exit(4); }
  log(`定时目标 ${m}-${DAY} ${HOUR}:${MINUTE}（距今 ${diffDays} 天，窗口内）`);
}

// ---------- CDP ----------
function getJSON(path) {
  return new Promise((res, rej) => {
    // Chrome 按 Host 头生成 webSocketDebuggerUrl，必须带 :9222，否则返回 ws://127.0.0.1/ 连到 80
    http.get({ host: '127.0.0.1', port: 9222, path, headers: { Host: '127.0.0.1:9222' } }, r => {
      let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });
}
// 找到含发布表单的 iframe（运行时探测，不要靠 URL 匹配）
const FIND_FORM = `(function(){var fs=Array.from(document.querySelectorAll('iframe'));
for(var i=0;i<fs.length;i++){var d=null;try{d=fs[i].contentDocument;}catch(e){}
if(d&&d.querySelector('input[type=file]'))return fs[i];}return null;})()`;

(async () => {
  const ver = await getJSON('/json/version');
  const ws = new WebSocket(ver.webSocketDebuggerUrl);
  let msgId = 1; const pending = new Map();
  let pageSession = null, fileBackendNode = null, mainUrl = null;

  function send(sessionId, method, params) {
    return new Promise((res, rej) => {
      const id = msgId++; pending.set(id, { res, rej });
      const msg = { id, method, params: params || {} };
      if (sessionId) msg.sessionId = sessionId; // null 会被 Chrome 拒
      ws.send(JSON.stringify(msg));
      setTimeout(() => { if (pending.has(id)) { pending.delete(id); rej(new Error('cmd timeout ' + method)); } }, 30000);
    });
  }
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  ws.on('message', m => {
    const o = JSON.parse(m);
    if (o.id && pending.has(o.id)) {
      const p = pending.get(o.id); pending.delete(o.id);
      if (o.error) p.rej(new Error(o.error.message)); else p.res(o.result); return;
    }
    if (o.method && o.sessionId === pageSession) {
      if (o.method === 'Page.frameNavigated' && !o.params.frame.parentId) mainUrl = o.params.frame.url;
      else if (o.method === 'Page.fileChooserOpened') fileBackendNode = o.params.backendNodeId;
    }
  });
  ws.on('error', e => { console.error('WSERR', e.message); process.exit(1); });

  // 顶层求值（不带 contextId，默认顶层框架）
  async function ev0(expr) {
    const r = await send(pageSession, 'Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error('eval0: ' + JSON.stringify(r.exceptionDetails).slice(0, 300));
    return r.result.value;
  }
  // 表单内求值：body 内可直接用 F(iframe) / D(document)
  async function ev(body) {
    return ev0(`(function(){var F=${FIND_FORM};if(!F)return '__NOFORM__';var D=F.contentDocument;${body}})()`);
  }
  async function clickAt(x, y) {
    await send(pageSession, 'Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
    await send(pageSession, 'Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
  }
  async function clickIn(fnStr) {
    const p = await ev0(`(function(){var F=${FIND_FORM};if(!F)return null;var D=F.contentDocument;
      var el=(${fnStr})(D); if(!el)return null;
      var fr=F.getBoundingClientRect(), r=el.getBoundingClientRect();
      return {x:fr.left+r.left+r.width/2,y:fr.top+r.top+r.height/2,w:r.width,h:r.height,frw:fr.width,frh:fr.height};})()`).catch(() => null);
    if (!p) return 'NO-ELEM';
    if (p.frw === 0 || p.frh === 0 || p.w === 0 || p.h === 0) return 'DOMCLICK';
    await clickAt(p.x, p.y); return 'clicked';
  }
  async function domClick(fnStr) {
    return ev(`var el=(${fnStr})(D); if(!el)return 'no-elem'; el.click(); return 'clicked';`).catch(e => 'err:' + e.message);
  }
  async function clickSmart(fnStr) {
    const r = await clickIn(fnStr);
    if (r === 'DOMCLICK' || r === 'NO-ELEM') await domClick(fnStr);
    return r;
  }
  const DLG_SEL = `(D)=>{var vis=function(el){var r=el.getBoundingClientRect();return r.width>100&&r.height>40;};
    var dlgs=Array.from(D.querySelectorAll('[class*=dialog],[class*=modal]')).filter(vis);
    if(!dlgs.length)return null;
    return dlgs.sort(function(a,b){var ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();return rb.width*rb.height-ra.width*ra.height;})[0];}`;
  const DLG_BTN = kw => `(D)=>{var d=(${DLG_SEL})(D);if(!d)return null;return Array.from(d.querySelectorAll('button,a,[class*=btn]')).find(x=>x.textContent.trim()===${JSON.stringify(kw)})||null;}`;
  const DLG_CB = `(D)=>{var d=(${DLG_SEL})(D);if(!d)return null;var cb=d.querySelector('input[type=checkbox]');if(!cb||cb.checked)return null;return cb.closest('.ant-checkbox')||cb.parentElement;}`;
  async function visDlg() {
    return ev(`var d=(${DLG_SEL})(D);return d?d.textContent.trim().slice(0,300):null;`).catch(() => null);
  }
  async function clickAbs(fnStr) {
    const p = await ev0(`(function(){var F=${FIND_FORM};if(!F)return null;var D=F.contentDocument;
      var el=(${fnStr})(D); if(!el)return null; el.scrollIntoView({block:'center'});
      var fr=F.getBoundingClientRect(), r=el.getBoundingClientRect();
      return {x:fr.left+r.left+r.width/2,y:fr.top+r.top+r.height/2};})()`).catch(() => null);
    if (!p) return 'NO-ELEM';
    await clickAt(p.x, p.y); return 'clicked';
  }

  // ---------- 连接并打开发布页 ----------
  await new Promise(res => ws.on('open', res));
  const cr = await send(null, 'Target.createTarget', { url: 'https://channels.weixin.qq.com/platform/post/create' });
  const at = await send(null, 'Target.attachToTarget', { targetId: cr.targetId, flatten: true });
  pageSession = at.sessionId;
  await send(null, 'Target.activateTarget', { targetId: cr.targetId }).catch(() => {});
  await send(pageSession, 'Page.enable');
  await send(pageSession, 'Runtime.enable');
  await send(pageSession, 'DOM.enable');
  await send(pageSession, 'Page.setInterceptFileChooserDialog', { enabled: true, cancel: false });
  log('已打开发布页');

  // 1) 等表单就绪
  let ready = false;
  for (let i = 0; i < 60; i++) {
    const has = await ev('return 1;').catch(() => '__NOFORM__');
    if (has !== '__NOFORM__') { ready = true; break; }
    const st = await ev0(`(function(){return {hasLogin:!!document.querySelector('iframe[src*="qrconnect"]')};})()`).catch(() => null);
    if (st && st.hasLogin) { log('❌ 登录态失效：请扫码登录后重跑'); ws.close(); process.exit(3); }
    await sleep(900);
  }
  if (!ready) { log('❌ 表单未就绪 url=' + (mainUrl || '?')); ws.close(); process.exit(1); }
  log('✅ 发布表单已就绪');

  // 2) 上传（objectId 直连，不依赖 file chooser）
  let uploaded = false;
  const inpRes = await send(pageSession, 'Runtime.evaluate', {
    expression: `(function(){var F=${FIND_FORM};if(!F)return null;var D=F.contentDocument;return D.querySelector('input[type=file]');})()`
  }).catch(() => null);
  const objId = inpRes && inpRes.result && inpRes.result.objectId;
  if (objId) {
    await send(pageSession, 'DOM.setFileInputFiles', { objectId: objId, files: [FILE] });
    uploaded = true; log('文件已注入（objectId 直连）');
  }
  if (!uploaded) {
    await domClick(`(D)=>D.querySelector('input[type=file]')`);
    for (let i = 0; i < 30; i++) {
      if (fileBackendNode) {
        await send(pageSession, 'DOM.setFileInputFiles', { backendNodeId: fileBackendNode, files: [FILE] });
        uploaded = true; log('文件已注入（file chooser 兜底）'); break;
      }
      await sleep(1000);
    }
  }
  if (!uploaded) { log('❌ 文件注入失败'); ws.close(); process.exit(1); }

  let ok = false;
  for (let i = 0; i < 200; i++) {
    const st = await ev(`var t=D.body.innerText;var v=D.querySelector('video');return {cover:/封面/.test(t),up:/上传中/.test(t),dur:v?v.duration:null};`).catch(() => null);
    if (st && st.cover && !st.up && st.dur) {
      if (!DURATION || Math.abs(st.dur - DURATION) < 10) { log(`✅ 上传完成 duration=${st.dur.toFixed(1)}s`); ok = true; break; }
    }
    await sleep(3000);
  }
  await send(pageSession, 'Page.setInterceptFileChooserDialog', { enabled: false }).catch(() => {});
  if (!ok) { log('❌ 上传未完成'); ws.close(); process.exit(1); }

  // 3) 短标题 / 描述 / 合集
  if (TITLE.length > 16) { log('❌ 短标题超 16 字:', TITLE.length); ws.close(); process.exit(1); }
  await ev(`var inp=D.querySelector('input[placeholder*="短标题"]');
    var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
    s.call(inp,${JSON.stringify(TITLE)});inp.dispatchEvent(new Event('input',{bubbles:true}));return inp.value;`);
  await sleep(300);
  if (DESC) {
    await ev(`var ed=D.querySelector('.input-editor');ed.scrollIntoView({block:'center'});ed.focus();
      document.execCommand('selectAll',false,null);document.execCommand('insertText',false,${JSON.stringify(DESC)});return 1;`);
  }
  await sleep(500);
  await domClick(`(D)=>D.querySelector('.post-album-display-wrap .display-text')`);
  await sleep(1500);
  await domClick(`(D)=>{var a=Array.from(D.querySelectorAll('.name')).find(n=>n.textContent.trim().includes(${JSON.stringify(ALBUM)}));return a?(a.closest('.item')||a.parentElement):null;}`);
  await sleep(1000);
  await send(pageSession, 'Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape' }).catch(() => {});
  await send(pageSession, 'Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape' }).catch(() => {});
  const albumTxt = await ev(`var w=D.querySelector('.post-album-display-wrap');return w?w.textContent.trim().slice(0,60):'';`).catch(() => '');
  log('字段完成 | 合集:', (albumTxt || '(未选中)').replace(/\s+/g, ' '));

  // 4) 定时
  if (!IMMEDIATE && DAY != null) {
    await ev(`var r=Array.from(D.querySelectorAll('input[type=radio]')).find(x=>x.value==='1');if(r&&!r.checked)r.click();return !!r;`);
    await sleep(1500);
    let hasTime = false;
    for (let i = 0; i < 20; i++) {
      hasTime = await ev(`return Array.from(D.querySelectorAll('.form-item')).some(x=>((x.querySelector('.label')||{}).textContent||'').trim().startsWith('发表时间'));`).catch(() => false);
      if (hasTime) break; await sleep(1000);
    }
    if (!hasTime) { log('❌ 未出现「发表时间」'); ws.close(); process.exit(1); }
    const TIME_INPUT = `(D)=>{var it=Array.from(D.querySelectorAll('.form-item')).find(x=>((x.querySelector('.label')||{}).textContent||'').trim().startsWith('发表时间'));if(!it)return null;return Array.from(it.querySelectorAll('input')).find(i=>i.getBoundingClientRect().width>0)||null;}`;
    let panelOpen = false;
    for (let i = 0; i < 10; i++) {
      panelOpen = await ev(`var dd=D.querySelector('.weui-desktop-picker__dd:not(.weui-desktop-picker__dd__time)');return !!(dd&&getComputedStyle(dd).display==='block');`).catch(() => false);
      if (panelOpen) break;
      await clickSmart(TIME_INPUT); await sleep(900);
    }
    if (!panelOpen) { log('❌ 日期面板未展开（新 UI 已知卡点，见 troubleshooting）'); ws.close(); process.exit(1); }
    const readMonth = () => ev(`var hd=D.querySelector('.weui-desktop-picker__panel__hd');var m=hd?hd.textContent.replace(/\\s/g,'').match(/(\\d{4})年(\\d{1,2})月/):null;return m?m[2]:null;`).catch(() => null);
    const NEXT = `(D)=>Array.from(D.querySelectorAll('button.weui-desktop-btn__icon__right')).find(x=>x.getBoundingClientRect().width>0)||null`;
    const wantMonth = MONTH ? String(MONTH) : String(new Date().getMonth() + 1 + (DAY < new Date().getDate() ? 1 : 0));
    for (let i = 0; i < 12; i++) {
      const m = await readMonth();
      if (m === wantMonth || m === String(MONTH || new Date().getMonth() + 1)) break;
      await clickSmart(NEXT); await sleep(700);
    }
    log('月份:', await readMonth());
    const DAY_FN = `(D)=>{var day=${DAY};return Array.from(D.querySelectorAll('.weui-desktop-picker__panel a')).find(x=>x.textContent.trim()===String(day)&&!/faded|disabled/.test(x.className))||null;}`;
    const dayR = await clickIn(DAY_FN);
    if (dayR === 'NO-ELEM') { log(`❌ 目标日 ${DAY} 不可选（超出可选窗口），已中止`); ws.close(); process.exit(4); }
    if (dayR === 'DOMCLICK') await domClick(DAY_FN);
    await sleep(800);
    const TV = `(D)=>D.querySelector('.weui-desktop-picker__time-value')`;
    await clickSmart(TV); await sleep(800);
    const pickLi = async (sel, val) => {
      const fn = `(D)=>{var ol=D.querySelector(${JSON.stringify(sel)});if(!ol)return null;return Array.from(ol.querySelectorAll('li')).find(l=>l.textContent.trim()===${JSON.stringify(val)})||null;}`;
      await clickSmart(fn); await sleep(500);
    };
    await pickLi('.weui-desktop-picker__time__hour', HOUR);
    await pickLi('.weui-desktop-picker__time__minute', MINUTE);
    const dateNow = await ev(`var i=Array.from(D.querySelectorAll('input')).find(x=>/^\\d{4}-\\d{1,2}-\\d{1,2}/.test(x.value));return i?i.value:null;`).catch(() => null);
    const timeNow = await ev(`var i=Array.from(D.querySelectorAll('input')).find(x=>/^\\d{1,2}:\\d{2}/.test(x.value));return i?i.value:null;`).catch(() => null);
    log('定时校验:', dateNow, timeNow);
    if (dateNow && !new RegExp(`-${DAY}$`).test(dateNow)) { log('❌ 日期不符预期，已中止'); ws.close(); process.exit(4); }
    if (timeNow && timeNow !== `${HOUR}:${MINUTE}`) { log('❌ 时间不符预期，已中止'); ws.close(); process.exit(4); }
    log('✅ 定时已设为', dateNow, timeNow);
  } else {
    await ev(`var r=Array.from(D.querySelectorAll('input[type=radio]')).find(x=>x.value==='0');if(r&&!r.checked)r.click();return !!r;`);
    log('即时发表模式（不定时）');
  }

  // 5) 声明原创
  await ev(`var cb=Array.from(D.querySelectorAll('input.ant-checkbox-input')).filter(c=>!c.checked)[0];if(cb)cb.click();return !!cb;`);
  await sleep(1800);
  const dlgTxt = await visDlg();
  if (dlgTxt && dlgTxt.includes('原创')) {
    await clickAbs(DLG_CB); await sleep(800);
    await clickAbs(DLG_BTN('声明原创')); await sleep(1800);
  }
  await sleep(1000);

  // 6) 保存草稿保底
  await domClick(`(D)=>Array.from(D.querySelectorAll('button')).find(x=>x.textContent.trim()==='保存草稿')||null`);
  await sleep(3000);

  if (DRY) { log('🧪 dry-run 模式：已填完并保存草稿，不点发表'); ws.close(); process.exit(0); }

  // 7) 发表 + 弹窗驱动
  const PUB = `(D)=>Array.from(D.querySelectorAll('button')).filter(x=>x.textContent.trim()==='发表'&&x.getBoundingClientRect().width>0).pop()||null`;
  const r0 = await clickSmart(PUB);
  log('点发表:', r0);
  let needQR = false, origHandled = false, extra = 0;
  for (let i = 0; i < 40; i++) {
    await sleep(1500);
    const d = await visDlg();
    if (!d) {
      if (origHandled && extra < 2) { extra++; await domClick(PUB); await sleep(2000); }
      continue;
    }
    if (d.includes('将此次编辑保留')) await clickAbs(DLG_BTN('不保存'));
    else if (d.includes('原创')) { await clickAbs(DLG_CB); await sleep(800); await clickAbs(DLG_BTN('声明原创')); origHandled = true; }
    else if (d.includes('广告分成')) { await clickAbs(DLG_BTN('直接发表')); await sleep(800); await clickAbs(DLG_BTN('声明原创')); }
    else if (d.includes('我知道了')) await clickAbs(DLG_BTN('我知道了'));
    else if (d.includes('管理员') || d.includes('实名') || d.includes('扫码')) { needQR = true; break; }
  }
  const isPublished = mainUrl && !mainUrl.includes('/post/create');
  log('结果:', isPublished ? '✅ PUBLISHED' : needQR ? '⚠️ NEED-QR' : '检查 URL=' + (mainUrl || '?'));
  ws.close();
  process.exit(isPublished ? 0 : needQR ? 2 : 1);
})().catch(e => { console.error('FATAL', e.stack); process.exit(1); });
