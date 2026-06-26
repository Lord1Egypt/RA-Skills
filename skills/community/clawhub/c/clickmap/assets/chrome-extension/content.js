(() => {
  let active = false;
  let marker = null;
  let hud = null;
  let dotsLayer = null;
  let lastMouse = { x: 0, y: 0, sx: 0, sy: 0 };

  const Z_MARKER = '2147483600';
  const Z_DOTS = '2147483601';
  const Z_HUD = '2147483646';
  const Z_TOAST = '2147483647';

  const loadPOIs = () => new Promise((resolve) => {
    chrome.storage.local.get(['clickmapPOIs'], (r) => {
      resolve(Array.isArray(r.clickmapPOIs) ? r.clickmapPOIs : []);
    });
  });

  const savePOI = (poi) => new Promise((resolve) => {
    chrome.storage.local.get(['clickmapPOIs'], (r) => {
      const list = Array.isArray(r.clickmapPOIs) ? r.clickmapPOIs : [];
      const filtered = list.filter(x => x.name !== poi.name);
      filtered.push(poi);
      chrome.storage.local.set({ clickmapPOIs: filtered }, () => resolve());
    });
  });

  const setPOIs = (pois) => new Promise((resolve) => {
    chrome.storage.local.set({ clickmapPOIs: pois }, () => resolve());
  });

  function cssPath(el) {
    if (!(el instanceof Element)) return '';
    const parts = [];
    while (el && el.nodeType === 1 && parts.length < 7) {
      let sel = el.nodeName.toLowerCase();
      if (el.id) { sel += `#${CSS.escape(el.id)}`; parts.unshift(sel); break; }
      const cls = [...el.classList].slice(0, 2).map(c => `.${CSS.escape(c)}`).join('');
      if (cls) sel += cls;
      parts.unshift(sel);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }

  function xPath(el) {
    if (!el || el.nodeType !== 1) return '';
    if (el.id) return `//*[@id="${el.id}"]`;
    const parts = [];
    while (el && el.nodeType === 1) {
      let i = 1;
      let sib = el.previousElementSibling;
      while (sib) { if (sib.nodeName === el.nodeName) i++; sib = sib.previousElementSibling; }
      parts.unshift(`${el.nodeName.toLowerCase()}[${i}]`);
      el = el.parentElement;
    }
    return '/' + parts.join('/');
  }

  function ensureMarker() {
    if (marker) return marker;
    marker = document.createElement('div');
    marker.id = '__clickmap_marker__';
    Object.assign(marker.style, {
      position: 'fixed',
      zIndex: Z_MARKER,
      pointerEvents: 'none',
      border: '2px solid #00e5ff',
      background: 'rgba(0,229,255,0.12)',
      borderRadius: '8px',
      display: 'none'
    });
    document.documentElement.appendChild(marker);
    return marker;
  }

  function ensureDotsLayer() {
    if (dotsLayer) return dotsLayer;
    dotsLayer = document.createElement('div');
    dotsLayer.id = '__clickmap_dots__';
    Object.assign(dotsLayer.style, {
      position: 'fixed',
      inset: '0',
      zIndex: Z_DOTS,
      pointerEvents: 'none'
    });
    document.documentElement.appendChild(dotsLayer);
    return dotsLayer;
  }

  async function renderDots() {
    const layer = ensureDotsLayer();
    layer.innerHTML = '';

    const pois = await loadPOIs();
    const here = `${location.origin}${location.pathname}`;
    const list = pois.filter(p => p?.coords?.viewport && (!p.urlPattern || p.urlPattern === here));

    for (const p of list) {
      const d = document.createElement('div');
      d.title = `${p.name} (${p.coords.viewport.x}, ${p.coords.viewport.y})`;
      Object.assign(d.style, {
        position: 'absolute',
        left: `${p.coords.viewport.x - 9}px`,
        top: `${p.coords.viewport.y - 9}px`,
        width: '18px',
        height: '18px',
        borderRadius: '50%',
        background: '#ff2ea6',
        border: '2px solid #ffd1ef',
        boxShadow: '0 0 0 3px #ff2ea650, 0 0 20px #ff2ea6'
      });
      layer.appendChild(d);
    }
  }

  function ensureHud() {
    if (hud) return hud;
    hud = document.createElement('div');
    hud.id = '__clickmap_hud__';
    hud.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#0f172acc;color:#e2e8f0;border:1px solid #38bdf8;border-radius:10px;font:12px/1.3 Inter,Segoe UI,Arial,sans-serif;box-shadow:0 8px 30px #0008;">
        <b style="color:#7dd3fc;">ClickMap ON</b>
        <span id="__clickmap_xy__">x: -, y: -</span>
        <span style="opacity:.9">Press <b>P</b> place • <b>D</b> delete nearest</span>
        <span style="opacity:.75">(Esc/F4 = off)</span>
        <button id="__clickmap_off__" style="margin-left:6px;cursor:pointer;border:1px solid #475569;background:#1e293b;color:#e2e8f0;border-radius:7px;padding:4px 8px;">Off</button>
      </div>
    `;
    Object.assign(hud.style, {
      position: 'fixed',
      top: '10px',
      left: '10px',
      zIndex: Z_HUD,
      pointerEvents: 'auto'
    });
    hud.addEventListener('click', (e) => e.stopPropagation(), true);
    document.documentElement.appendChild(hud);

    const offBtn = hud.querySelector('#__clickmap_off__');
    const offNow = (e) => { e.preventDefault(); e.stopPropagation(); disable(); };
    offBtn?.addEventListener('pointerdown', offNow, true);
    offBtn?.addEventListener('click', offNow, true);

    return hud;
  }

  function updateHudXY(x, y) {
    const el = hud?.querySelector('#__clickmap_xy__');
    if (el) el.textContent = `x: ${Math.round(x)}, y: ${Math.round(y)}`;
  }

  function isOwnUI(el) {
    return !!(el && (el.closest('#__clickmap_hud__') || el.closest('#__clickmap_toast__')));
  }

  function showToast(text) {
    let t = document.getElementById('__clickmap_toast__');
    if (!t) {
      t = document.createElement('div');
      t.id = '__clickmap_toast__';
      Object.assign(t.style, {
        position: 'fixed',
        right: '14px',
        top: '14px',
        zIndex: Z_TOAST,
        background: '#052e16ee',
        color: '#dcfce7',
        border: '1px solid #22c55e',
        borderRadius: '10px',
        padding: '9px 12px',
        font: '12px Inter,Segoe UI,Arial,sans-serif',
        boxShadow: '0 8px 30px #0008',
        pointerEvents: 'none'
      });
      document.documentElement.appendChild(t);
    }
    t.textContent = text;
    t.style.display = 'block';
    clearTimeout(t._tmr);
    t._tmr = setTimeout(() => { t.style.display = 'none'; }, 2200);
  }

  function onMove(e) {
    if (!active) return;
    lastMouse = { x: e.clientX, y: e.clientY, sx: e.screenX, sy: e.screenY };
    updateHudXY(e.clientX, e.clientY);

    const el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || isOwnUI(el)) return;

    const r = el.getBoundingClientRect();
    const m = ensureMarker();
    m.style.display = 'block';
    m.style.left = `${r.left}px`;
    m.style.top = `${r.top}px`;
    m.style.width = `${r.width}px`;
    m.style.height = `${r.height}px`;
  }

  async function placePointAtMouse() {
    const { x, y, sx, sy } = lastMouse;
    const el = document.elementFromPoint(x, y);
    if (!el || isOwnUI(el)) return;

    const defaultName = `${location.hostname.replace(/\W+/g, '_')}.${el.tagName.toLowerCase()}`;
    const name = window.prompt(`Save POI at viewport x:${Math.round(x)}, y:${Math.round(y)}\nScreen x:${Math.round(sx)}, y:${Math.round(sy)}\nEnter POI name:`, defaultName);
    if (name == null) {
      showToast('Cancelled');
      return;
    }

    const clean = name.trim();
    if (!clean) {
      showToast('POI name required');
      return;
    }

    const r = el.getBoundingClientRect();
    const poi = {
      id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`,
      name: clean,
      urlPattern: `${location.origin}${location.pathname}`,
      coords: {
        viewport: { x: Math.round(x), y: Math.round(y) },
        screen: { x: Math.round(sx), y: Math.round(sy) },
        page: { x: Math.round(window.scrollX + x), y: Math.round(window.scrollY + y) },
        rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }
      },
      selectors: {
        css: cssPath(el),
        xpath: xPath(el),
        id: el.id || '',
        role: el.getAttribute('role') || '',
        ariaLabel: el.getAttribute('aria-label') || '',
        text: (el.innerText || el.textContent || '').trim().slice(0, 120)
      },
      meta: {
        tag: el.tagName.toLowerCase(),
        zoom: window.devicePixelRatio || 1,
        viewport: { w: window.innerWidth, h: window.innerHeight },
        savedAt: new Date().toISOString()
      }
    };

    await savePOI(poi);
    await renderDots();
    showToast(`✅ Stored ${poi.name} @ x:${poi.coords.viewport.x}, y:${poi.coords.viewport.y}`);
    console.log('[ClickMap] saved POI:', poi.name, poi);

    try {
      chrome.runtime.sendMessage({ type: 'CLICKMAP_SYNC_NOW' });
    } catch {}
  }

  async function removeNearestPointAtMouse() {
    const { x, y } = lastMouse;
    const here = `${location.origin}${location.pathname}`;
    const pois = await loadPOIs();

    let nearest = null;
    for (const p of pois) {
      if (p?.urlPattern && p.urlPattern !== here) continue;
      const px = p?.coords?.viewport?.x;
      const py = p?.coords?.viewport?.y;
      if (px == null || py == null) continue;
      const d = Math.hypot(px - x, py - y);
      if (!nearest || d < nearest.distance) {
        nearest = { poi: p, distance: d };
      }
    }

    if (!nearest || nearest.distance > 24) {
      showToast('No POI near cursor to delete');
      return;
    }

    const target = nearest.poi;
    const remaining = pois.filter((p) => {
      if (target.id && p.id) return p.id !== target.id;
      return !(p.name === target.name && p?.coords?.viewport?.x === target?.coords?.viewport?.x && p?.coords?.viewport?.y === target?.coords?.viewport?.y);
    });

    await setPOIs(remaining);
    await renderDots();
    showToast(`🗑 Removed ${target.name}`);
    try {
      chrome.runtime.sendMessage({ type: 'CLICKMAP_SYNC_NOW' });
    } catch {}
  }

  function onKeyDown(e) {
    if (!active) return;

    if (e.key === 'Escape' || e.key === 'F4') {
      e.preventDefault();
      disable();
      return;
    }

    if (e.key.toLowerCase() === 'd') {
      e.preventDefault();
      removeNearestPointAtMouse();
      return;
    }

    if (e.key.toLowerCase() === 'p') {
      e.preventDefault();
      placePointAtMouse();
      return;
    }
  }

  function notifyState() {
    try { chrome.runtime.sendMessage({ type: 'CLICKMAP_MARKING_STATE', active }); } catch {}
  }

  async function enable() {
    if (active) return;
    active = true;
    ensureHud();
    ensureMarker();
    ensureDotsLayer();
    document.addEventListener('mousemove', onMove, true);
    document.addEventListener('keydown', onKeyDown, true);
    document.documentElement.style.cursor = 'crosshair';
    hud.style.display = 'block';
    dotsLayer.style.display = 'block';
    await renderDots();
    notifyState();
  }

  function disable() {
    active = false;
    document.removeEventListener('mousemove', onMove, true);
    document.removeEventListener('keydown', onKeyDown, true);
    document.documentElement.style.cursor = '';
    if (marker) marker.style.display = 'none';
    if (hud) hud.style.display = 'none';
    if (dotsLayer) dotsLayer.style.display = 'none';
    notifyState();
  }

  async function toggle() {
    if (active) disable(); else await enable();
    return active;
  }

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === 'local' && changes.clickmapPOIs && active) renderDots();
  });

  chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
    if (msg?.type === 'CLICKMAP_START') { enable().then(() => sendResponse({ ok: true, active })); return true; }
    if (msg?.type === 'CLICKMAP_STOP') { disable(); sendResponse({ ok: true, active }); return; }
    if (msg?.type === 'CLICKMAP_TOGGLE') { toggle().then((a) => sendResponse({ ok: true, active: a })); return true; }
    if (msg?.type === 'CLICKMAP_PING') { sendResponse({ ok: true, active, url: location.href }); return; }
  });
})();
