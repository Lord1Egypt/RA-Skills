const { chromium } = require('playwright-core');
const fs = require('fs');

// 用法: node cdp-resched.js <ep> <月> <日> <时> <分>
// 已定时未发布的条目改时间：列表 → 修改并重新发表 → 补描述 → 重设定时 → 发表
const EP = Number(process.argv[2]);
const TARGET_MONTH = process.argv[3];
const TARGET_DAY = process.argv[4];
const TARGET_HOUR = process.argv[5];
const TARGET_MIN = process.argv[6] || '00';
if (!EP || !TARGET_MONTH || !TARGET_DAY || !TARGET_HOUR) { console.error('用法: node cdp-resched.js <ep> <月> <日> <时> [分]'); process.exit(1); }
const conf = JSON.parse(fs.readFileSync(__dirname + '/episodes.json', 'utf8')).find(e => e.ep === EP);
if (!conf) { console.error('找不到 ep' + EP); process.exit(1); }
const log = (...a) => console.log(`[ep${EP}]`, ...a);

const visDlg = (frame) => frame.evaluate(() => {
  const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 100 && r.height > 40; };
  const dlgs = Array.from(document.querySelectorAll('[class*=dialog], [class*=modal]')).filter(vis);
  if (!dlgs.length) return null;
  const d = dlgs.sort((a, b) => { const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(); return rb.width * rb.height - ra.width * ra.height; })[0];
  return d.textContent.trim().slice(0, 300);
});
const dlgBtn = (frame, kw) => frame.evaluate((kw) => {
  const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 100 && r.height > 40; };
  const dlgs = Array.from(document.querySelectorAll('[class*=dialog], [class*=modal]')).filter(vis);
  if (!dlgs.length) return 'no-dlg';
  const d = dlgs.sort((a, b) => { const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(); return rb.width * rb.height - ra.width * ra.height; })[0];
  const b = Array.from(d.querySelectorAll('button, a, [class*=btn]')).find(x => x.textContent.trim() === kw);
  if (!b) return 'no-btn';
  b.click();
  return 'clicked:' + kw;
}, kw);
async function clickDlgCheckbox(page, frame) {
  for (let attempt = 0; attempt < 3; attempt++) {
    const pos = await frame.evaluate(() => {
      const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 100 && r.height > 40; };
      const dlgs = Array.from(document.querySelectorAll('[class*=dialog], [class*=modal]')).filter(vis);
      if (!dlgs.length) return null;
      const d = dlgs.sort((a, b) => { const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(); return rb.width * rb.height - ra.width * ra.height; })[0];
      const cb = d.querySelector('input[type=checkbox]');
      if (!cb) return null;
      const target = cb.closest('.ant-checkbox') || cb.parentElement;
      const r = target.getBoundingClientRect();
      const ir = cb.getBoundingClientRect();
      const box = ir.width > 0 ? ir : r;
      return { x: box.x + box.width / 2, y: box.y + box.height / 2, checked: cb.checked };
    });
    if (!pos) return 'no-cb';
    if (pos.checked) return 'already-checked';
    await page.mouse.click(pos.x, pos.y);
    await page.waitForTimeout(600);
    const now = await frame.evaluate(() => {
      const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 100 && r.height > 40; };
      const dlgs = Array.from(document.querySelectorAll('[class*=dialog], [class*=modal]')).filter(vis);
      if (!dlgs.length) return null;
      const d = dlgs.sort((a, b) => { const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(); return rb.width * rb.height - ra.width * ra.height; })[0];
      const cb = d.querySelector('input[type=checkbox]');
      return cb ? cb.checked : null;
    });
    if (now) return 'clicked-ok';
  }
  return 'failed';
}
async function dlgBtnReal(page, frame, kw) {
  const pos = await frame.evaluate((kw) => {
    const vis = (el) => { const r = el.getBoundingClientRect(); return r.width > 100 && r.height > 40; };
    const dlgs = Array.from(document.querySelectorAll('[class*=dialog], [class*=modal]')).filter(vis);
    if (!dlgs.length) return null;
    const d = dlgs.sort((a, b) => { const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(); return rb.width * rb.height - ra.width * ra.height; })[0];
    const b = Array.from(d.querySelectorAll('button, a, [class*=btn]')).find(x => x.textContent.trim() === kw);
    if (!b) return { err: 'no-btn' };
    b.scrollIntoView({ block: 'center' });
    const r = b.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2, disabled: (b.className || '').includes('disabled') };
  }, kw);
  if (!pos) return 'no-dlg';
  if (pos.err) return pos.err;
  if (pos.disabled) return 'BTN-DISABLED';
  await page.mouse.click(pos.x, pos.y);
  return 'real-clicked:' + kw;
}
async function clickAt(page, frame, pos, wantSel) {
  const hit = await frame.evaluate(({ x, y, wantSel }) => {
    const el = document.elementFromPoint(x, y);
    if (!el) return { ok: false, got: 'null' };
    const want = document.querySelector(wantSel);
    const ok = want ? (el === want || want.contains(el) || el.contains(want)) : false;
    return { ok, got: el.tagName + '.' + (el.className || '').toString().slice(0, 40) };
  }, { x: pos.x, y: pos.y, wantSel });
  if (!hit.ok) { log('⚠️ 点击被遮挡，命中:', hit.got); return false; }
  await page.mouse.click(pos.x, pos.y);
  return true;
}

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const ctx = browser.contexts()[0];

  // 1) 列表页 → 修改并重新发表
  const page = await ctx.newPage();
  await page.goto('https://channels.weixin.qq.com/platform/post/list', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(8000);
  const lf = page.frames().find(f => f.url().includes('/micro/content/post/list'));
  const clicked = await lf.evaluate((epTag) => {
    let card = null;
    document.querySelectorAll('div').forEach(d => {
      const t = d.textContent || '';
      if (t.includes(epTag) && t.includes('修改并重新发表') && t.length < 1500) {
        if (!card || t.length < card.textContent.length) card = d;
      }
    });
    if (!card) return 'card-not-found';
    const b = Array.from(card.querySelectorAll('*')).find(e => e.children.length === 0 && e.textContent.trim() === '修改并重新发表');
    if (!b) return 'btn-not-found';
    b.click();
    return 'clicked';
  }, `第${EP}期`);
  log('进编辑:', clicked);
  if (clicked !== 'clicked') { process.exit(1); }

  for (let i = 0; i < 25; i++) { await page.waitForTimeout(1000); if (page.url().includes('/post/create')) break; }
  const frame = page.frames().find(f => f.url().includes('/micro/content/post/create'));
  let hasCover = false;
  for (let i = 0; i < 20; i++) {
    hasCover = await frame.evaluate(() => document.body.innerText.includes('封面预览'));
    if (hasCover) break;
    await page.waitForTimeout(1000);
  }
  if (!hasCover) { log('❌ 编辑页无视频，中止'); process.exit(1); }
  log('编辑页就绪');

  const snap = () => frame.evaluate(() => ({
    title: (document.querySelector('input[placeholder*="短标题"]') || {}).value || '',
    descLen: ((document.querySelector('.input-editor') || {}).textContent || '').length,
    orig: (document.querySelector('input.ant-checkbox-input') || {}).checked,
    radio: (Array.from(document.querySelectorAll('input[type=radio]')).find(r => r.checked) || {}).value,
  }));
  const s = await snap();
  log('快照:', JSON.stringify(s));

  // 2) 补描述 / 标题（编辑页会丢）
  if (s.descLen < 50) {
    await frame.evaluate((d) => {
      const ed = document.querySelector('.input-editor');
      ed.scrollIntoView({ block: 'center' }); ed.focus();
      document.execCommand('selectAll', false, null);
      document.execCommand('insertText', false, d);
    }, conf.desc);
    await page.waitForTimeout(600);
    log('已补描述:', (await snap()).descLen);
  }
  if (!(await snap()).title) {
    await frame.evaluate((t) => {
      const inp = document.querySelector('input[placeholder*="短标题"]');
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(inp, t);
      inp.dispatchEvent(new Event('input', { bubbles: true }));
    }, conf.title);
    log('已补标题');
  }

  // 3) 重新设定时（真实点击链路，复用 cdp-publish-one 验证过的逻辑）
  const readMonth = () => frame.evaluate(() => {
    const hd = document.querySelector('.weui-desktop-picker__panel__hd');
    const m = hd ? hd.textContent.replace(/\s/g, '').match(/(\d{4})年(\d{1,2})月/) : null;
    return m ? m[2] : null;
  });
  const timeVal = () => frame.evaluate(() => {
    const i = Array.from(document.querySelectorAll('input')).find(x => /^\d{1,2}:\d{2}/.test(x.value));
    return i ? i.value : null;
  });

  let hasTimeItem = false;
  for (let i = 0; i < 15; i++) {
    hasTimeItem = await frame.evaluate(() => Array.from(document.querySelectorAll('.form-item'))
      .some(x => (x.querySelector('.label') || {}).textContent?.trim().startsWith('发表时间')));
    if (hasTimeItem) break;
    await page.waitForTimeout(1000);
  }
  if (!hasTimeItem) {
    // radio 可能没带出来，重新点定时 radio
    await frame.evaluate(() => {
      const r = Array.from(document.querySelectorAll('input[type=radio]')).find(x => x.value === '1');
      if (r && !r.checked) r.click();
    });
    await page.waitForTimeout(1500);
    hasTimeItem = await frame.evaluate(() => Array.from(document.querySelectorAll('.form-item'))
      .some(x => (x.querySelector('.label') || {}).textContent?.trim().startsWith('发表时间')));
  }
  if (!hasTimeItem) { log('❌ 「发表时间」表单项未出现，中止'); process.exit(1); }

  const getDateBox = () => frame.evaluate(() => {
    const items = Array.from(document.querySelectorAll('.form-item'));
    const it = items.find(x => (x.querySelector('.label') || {}).textContent?.trim().startsWith('发表时间'));
    if (!it) return null;
    it.scrollIntoView({ block: 'center' });
    const vis = Array.from(it.querySelectorAll('input')).filter(i => i.getBoundingClientRect().width > 0);
    if (!vis.length) return null;
    const inp = vis.find(i => /^\d{4}-\d{1,2}-\d{1,2}/.test(i.value)) || vis[0];
    const r = inp.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2, cls: inp.className };
  });

  let panelOpen = false;
  for (let i = 0; i < 10; i++) {
    panelOpen = await frame.evaluate(() => {
      const dd = document.querySelector('.weui-desktop-picker__dd:not(.weui-desktop-picker__dd__time)');
      return !!(dd && getComputedStyle(dd).display === 'block');
    });
    if (panelOpen) break;
    const box = await getDateBox();
    if (!box) { await page.waitForTimeout(700); continue; }
    await clickAt(page, frame, box, '.weui-desktop-picker__value_input');
    await page.waitForTimeout(900);
  }
  if (!panelOpen) { log('❌ 日期面板未展开'); process.exit(1); }

  for (let i = 0; i < 12; i++) {
    const m = await readMonth();
    if (m === String(Number(TARGET_MONTH))) break;
    const bp = await frame.evaluate(() => {
      const b = Array.from(document.querySelectorAll('button.weui-desktop-btn__icon__right')).find(x => x.getBoundingClientRect().width > 0);
      if (!b) return null;
      const r = b.getBoundingClientRect();
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
    });
    if (!bp) { await page.waitForTimeout(800); continue; }
    await page.mouse.click(bp.x, bp.y);
    await page.waitForTimeout(600);
  }
  log('月份:', await readMonth());

  const dayPos = await frame.evaluate((day) => {
    const a = Array.from(document.querySelectorAll('.weui-desktop-picker__panel a'))
      .find(x => x.textContent.trim() === String(day) && !/faded|disabled/.test(x.className));
    if (!a) return null;
    const r = a.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  }, TARGET_DAY);
  if (!dayPos) { log('❌ 找不到可点日期', TARGET_DAY); process.exit(1); }
  await page.mouse.click(dayPos.x, dayPos.y);
  await page.waitForTimeout(700);

  let tvPos = await frame.evaluate(() => {
    const tv = document.querySelector('.weui-desktop-picker__time-value');
    if (!tv) return null;
    const r = tv.getBoundingClientRect();
    return r.width > 0 ? { x: r.x + r.width / 2, y: r.y + r.height / 2 } : null;
  });
  if (tvPos) { await page.mouse.click(tvPos.x, tvPos.y); await page.waitForTimeout(700); }
  if (!(await frame.evaluate(() => {
    const dd = document.querySelector('.weui-desktop-picker__dd__time');
    return dd && getComputedStyle(dd).display === 'block';
  }))) {
    tvPos = await frame.evaluate(() => {
      const ic = document.querySelector('.weui-desktop-icon__time');
      const b = ic && (ic.closest('button') || ic);
      const r = b.getBoundingClientRect();
      return r.width > 0 ? { x: r.x + r.width / 2, y: r.y + r.height / 2 } : null;
    });
    if (tvPos) { await page.mouse.click(tvPos.x, tvPos.y); await page.waitForTimeout(700); }
  }

  // 时间面板展开（可重复调用）
  const openTimePanel = async () => {
    if (await frame.evaluate(() => {
      const dd = document.querySelector('.weui-desktop-picker__dd__time');
      return dd && getComputedStyle(dd).display === 'block';
    })) return true;
    let p = await frame.evaluate(() => {
      const tv = document.querySelector('.weui-desktop-picker__time-value');
      if (!tv) return null;
      const r = tv.getBoundingClientRect();
      return r.width > 0 ? { x: r.x + r.width / 2, y: r.y + r.height / 2 } : null;
    });
    if (p) { await page.mouse.click(p.x, p.y); await page.waitForTimeout(700); }
    if (await frame.evaluate(() => {
      const dd = document.querySelector('.weui-desktop-picker__dd__time');
      return dd && getComputedStyle(dd).display === 'block';
    })) return true;
    p = await frame.evaluate(() => {
      const ic = document.querySelector('.weui-desktop-icon__time');
      const b = ic && (ic.closest('button') || ic);
      const r = b.getBoundingClientRect();
      return r.width > 0 ? { x: r.x + r.width / 2, y: r.y + r.height / 2 } : null;
    });
    if (p) { await page.mouse.click(p.x, p.y); await page.waitForTimeout(700); }
    return await frame.evaluate(() => {
      const dd = document.querySelector('.weui-desktop-picker__dd__time');
      return dd && getComputedStyle(dd).display === 'block';
    });
  };

  const pickLi = async (sel, val) => {
    let pos = await frame.evaluate(({ sel, val }) => {
      const ol = document.querySelector(sel);
      if (!ol) return null;
      const li = Array.from(ol.querySelectorAll('li')).find(l => l.textContent.trim() === val);
      if (!li) return null;
      ol.scrollTop = li.offsetTop - ol.clientHeight / 2;
      const r = li.getBoundingClientRect();
      return { x: r.x + r.width / 2, y: r.y + r.height / 2, vh: window.innerHeight };
    }, { sel, val });
    if (!pos) return false;
    if (pos.y < 0 || pos.y > pos.vh) {
      await frame.evaluate(({ sel, val }) => {
        const ol = document.querySelector(sel);
        const li = Array.from(ol.querySelectorAll('li')).find(l => l.textContent.trim() === val);
        li.scrollIntoView({ block: 'center' });
      }, { sel, val });
      await page.waitForTimeout(400);
      pos = await frame.evaluate(({ sel, val }) => {
        const ol = document.querySelector(sel);
        const li = Array.from(ol.querySelectorAll('li')).find(l => l.textContent.trim() === val);
        const r = li.getBoundingClientRect();
        return { x: r.x + r.width / 2, y: r.y + r.height / 2, vh: window.innerHeight };
      }, { sel, val });
    }
    if (pos.y < 0 || pos.y > pos.vh) return false;
    await page.mouse.click(pos.x, pos.y);
    await page.waitForTimeout(400);
    return true;
  };
  // 点 hour/minute 带重试（07 在滚动列表边缘时点击偶发不生效，9-20 已知问题）
  for (let i = 0; i < 6; i++) {
    if (!(await openTimePanel())) { log('⚠️ 时间面板打不开，重试', i + 1); continue; }
    await pickLi('.weui-desktop-picker__time__hour', TARGET_HOUR);
    await page.waitForTimeout(400);
    if (!(await openTimePanel())) continue;
    await pickLi('.weui-desktop-picker__time__minute', TARGET_MIN);
    await page.waitForTimeout(400);
    const cur = await timeVal();
    if (cur === `${TARGET_HOUR}:${TARGET_MIN}`) break;
    log(`  时间重试 #${i + 1}: 当前 ${cur}`);
  }
  const tv = await timeVal();
  log('时间校验:', tv, tv === `${TARGET_HOUR}:${TARGET_MIN}` ? '✅' : '❌');
  if (tv !== `${TARGET_HOUR}:${TARGET_MIN}`) { log('❌ 时间不对，中止'); process.exit(1); }

  // 4) 原创应已勾上；没勾就补
  if (!(await snap()).orig) {
    await frame.evaluate(() => {
      const cb = document.querySelector('input.ant-checkbox-input');
      if (cb && !cb.checked) cb.click();
    });
    await page.waitForTimeout(1500);
    const dlg = await visDlg(frame);
    if (dlg && dlg.includes('原创权益')) {
      log('勾同意:', await clickDlgCheckbox(page, frame));
      await page.waitForTimeout(800);
      log('声明原创:', await dlgBtnReal(page, frame, '声明原创'));
      await page.waitForTimeout(1500);
    }
  }
  const origOk = await frame.evaluate(() => (document.querySelector('input.ant-checkbox-input') || {}).checked);
  log('原创:', origOk ? '✅' : '❌');
  if (!origOk) { log('❌ 原创未勾上，中止'); process.exit(1); }

  // 5) 发表 + 弹窗驱动（全程不 goto）
  await frame.evaluate(() => {
    const b = Array.from(document.querySelectorAll('button'))
      .filter(x => x.textContent.trim() === '发表' && x.getBoundingClientRect().width > 0).pop();
    b.scrollIntoView({ block: 'center' });
  });
  await page.waitForTimeout(500);
  const clickRes = await frame.evaluate(() => {
    const b = Array.from(document.querySelectorAll('button'))
      .filter(x => x.textContent.trim() === '发表' && x.getBoundingClientRect().width > 0).pop();
    if ((b.className || '').includes('disabled')) return 'DISABLED';
    b.click();
    return 'clicked';
  });
  log('点发表:', clickRes);
  if (clickRes === 'DISABLED') { log('❌ 发表按钮禁用'); process.exit(1); }

  let published = false, origHandled = false, extraClicks = 0;
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(1500);
    if (!page.url().includes('/post/create')) { published = true; break; }
    const dlg = await visDlg(frame);
    if (!dlg) {
      if (origHandled && extraClicks < 2) {
        extraClicks++;
        log('  → 补点发表 #' + extraClicks);
        await frame.evaluate(() => {
          const b = Array.from(document.querySelectorAll('button'))
            .filter(x => x.textContent.trim() === '发表' && x.getBoundingClientRect().width > 0 && !(x.className || '').includes('disabled')).pop();
          if (b) b.click();
        });
        await page.waitForTimeout(2000);
      }
      continue;
    }
    log('弹窗:', dlg.replace(/\n/g, ' ').slice(0, 60));
    if (dlg.includes('将此次编辑保留')) log('  →', await dlgBtn(frame, '不保存'));
    else if (dlg.includes('原创权益')) {
      log('  → 勾同意:', await clickDlgCheckbox(page, frame));
      await page.waitForTimeout(800);
      log('  →', await dlgBtnReal(page, frame, '声明原创'));
      origHandled = true;
    } else if (dlg.includes('广告分成')) {
      let r = await dlgBtn(frame, '直接发表');
      if (!r.startsWith('clicked')) r = await dlgBtn(frame, '声明原创');
      log('  →', r);
    } else if (dlg.includes('我知道了')) log('  →', await dlgBtn(frame, '我知道了'));
  }
  log('结果:', published ? '✅ PUBLISHED' : '❌ URL=' + page.url());
  await page.close().catch(() => {});
  process.exit(published ? 0 : 1);
})().catch(e => { console.error('FATAL', e.stack); process.exit(1); });
