const $ = (id) => document.getElementById(id);
const OPTIONS_URL = chrome.runtime.getURL('options.html');

async function activeTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

function setText(id, text, ok) {
  const el = $(id);
  el.textContent = text;
  el.classList.remove('ok', 'bad');
  el.classList.add(ok ? 'ok' : 'bad');
}

function status(t) { $('status').textContent = t; }

function renderSavedForPage(tabUrl) {
  const list = $('savedList');
  if (!list) return;
  list.innerHTML = '';

  let here = '';
  try {
    const u = new URL(tabUrl || '');
    here = `${u.origin}${u.pathname}`;
  } catch {
    const li = document.createElement('li');
    li.textContent = 'Open a website tab';
    list.appendChild(li);
    return;
  }

  chrome.storage.local.get(['clickmapPOIs'], (r) => {
    const pois = (Array.isArray(r.clickmapPOIs) ? r.clickmapPOIs : [])
      .filter(p => p?.urlPattern === here)
      .slice(-20)
      .reverse();

    if (!pois.length) {
      const li = document.createElement('li');
      li.textContent = 'No POIs yet';
      list.appendChild(li);
      return;
    }

    for (const p of pois) {
      const x = p?.coords?.viewport?.x ?? '-';
      const y = p?.coords?.viewport?.y ?? '-';
      const li = document.createElement('li');
      li.textContent = `${p.name} (${x}, ${y})`;
      list.appendChild(li);
    }
  });
}

async function ensureContentScript(tabId) {
  try {
    await chrome.tabs.sendMessage(tabId, { type: 'CLICKMAP_PING' });
    return true;
  } catch {
    try {
      await chrome.scripting.executeScript({ target: { tabId }, files: ['content.js'] });
      await chrome.tabs.sendMessage(tabId, { type: 'CLICKMAP_PING' });
      return true;
    } catch {
      return false;
    }
  }
}

async function checkState() {
  let tabOk = false;
  let bridgeOk = false;
  let currentTabUrl = '';

  try {
    const tab = await activeTab();
    currentTabUrl = tab?.url || '';
    if (tab?.id && /^https?:/i.test(tab.url || '')) {
      tabOk = await ensureContentScript(tab.id);
    }
    setText('tabState', tabOk ? 'connected' : 'not connected', tabOk);
  } catch {
    setText('tabState', 'not connected', false);
  }

  renderSavedForPage(currentTabUrl);

  chrome.storage.local.get(['clickmapBridge', 'clickmapPOIs'], async (r) => {
    const bridge = r.clickmapBridge || { url: 'http://127.0.0.1:18795', token: '' };
    const pois = Array.isArray(r.clickmapPOIs) ? r.clickmapPOIs.length : 0;
    try {
      const resp = await fetch(`${bridge.url}/health`, {
        headers: bridge.token ? { 'X-ClickMap-Token': bridge.token } : {}
      });
      bridgeOk = resp.ok;
      setText('bridgeState', bridgeOk ? 'online' : 'offline', bridgeOk);
    } catch {
      setText('bridgeState', 'offline', false);
    }

    const agentOk = tabOk && bridgeOk;
    setText('agentState', agentOk ? `ready (${pois} POIs)` : 'not ready', agentOk);
  });
}

$('open').onclick = async () => {
  await chrome.tabs.create({ url: OPTIONS_URL, active: true });
  window.close();
};

$('toggle').onclick = async () => {
  try {
    const tab = await activeTab();
    if (!tab?.id || !/^https?:/i.test(tab.url || '')) {
      status('Open a normal website tab first (https://...)');
      return;
    }
    const ok = await ensureContentScript(tab.id);
    if (!ok) {
      status('Tab hook failed. Reload page, then try again.');
      await checkState();
      return;
    }
    const out = await chrome.tabs.sendMessage(tab.id, { type: 'CLICKMAP_TOGGLE' });
    status(out?.active ? 'Marking ON (press P to place)' : 'Marking OFF');
    await checkState();
  } catch (e) {
    status(`Toggle failed: ${e.message}`);
  }
};

$('sync').onclick = () => {
  chrome.storage.local.get(['clickmapPOIs', 'clickmapBridge'], async (r) => {
    const pois = r.clickmapPOIs || [];
    const bridge = r.clickmapBridge || { url: 'http://127.0.0.1:18795', token: '' };
    try {
      const resp = await fetch(`${bridge.url}/api/pois`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(bridge.token ? { 'X-ClickMap-Token': bridge.token } : {})
        },
        body: JSON.stringify({ pois })
      });
      const out = await resp.json();
      if (!resp.ok) throw new Error(out.error || 'sync_failed');
      status(`Synced ${out.count} POIs`);
      await checkState();
    } catch (e) {
      status(`Sync failed: ${e.message}`);
      await checkState();
    }
  });
};

chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'local' && changes.clickmapPOIs) checkState();
});

checkState();
setInterval(checkState, 2000);
