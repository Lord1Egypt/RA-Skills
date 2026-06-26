const OPTIONS_URL = chrome.runtime.getURL('options.html');

async function openConfigTab() {
  const tabs = await chrome.tabs.query({});
  const existing = tabs.find(t => t.url && t.url.startsWith(OPTIONS_URL));
  if (existing?.id) {
    await chrome.tabs.update(existing.id, { active: true });
    return;
  }
  await chrome.tabs.create({ url: OPTIONS_URL, active: true });
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

function getStorage(keys) {
  return new Promise((resolve) => chrome.storage.local.get(keys, resolve));
}

async function syncPoisToBridge() {
  const state = await getStorage(['clickmapPOIs', 'clickmapBridge']);
  const pois = Array.isArray(state.clickmapPOIs) ? state.clickmapPOIs : [];
  const bridge = state.clickmapBridge || { url: 'http://127.0.0.1:18795', token: '' };

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
  return out;
}

async function toggleMarkingOnActiveTab() {
  const tab = await getActiveTab();
  if (!tab?.id) return;
  try {
    const res = await chrome.tabs.sendMessage(tab.id, { type: 'CLICKMAP_TOGGLE' });
    const on = !!res?.active;
    await chrome.action.setBadgeText({ tabId: tab.id, text: on ? 'ON' : '' });
    await chrome.action.setBadgeBackgroundColor({ tabId: tab.id, color: '#3b82f6' });
  } catch {
    await chrome.action.setBadgeText({ tabId: tab.id, text: 'ERR' });
    await chrome.action.setBadgeBackgroundColor({ tabId: tab.id, color: '#ef4444' });
  }
}

chrome.runtime.onInstalled.addListener(async () => {
  chrome.storage.local.get(['clickmapPOIs', 'clickmapBridge'], (r) => {
    if (!Array.isArray(r.clickmapPOIs)) chrome.storage.local.set({ clickmapPOIs: [] });
    if (!r.clickmapBridge) chrome.storage.local.set({ clickmapBridge: { url: 'http://127.0.0.1:18795', token: '' } });
  });
  await openConfigTab();
});

chrome.commands.onCommand.addListener(async (command) => {
  if (command === 'toggle-marking') {
    await toggleMarkingOnActiveTab();
  }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === 'CLICKMAP_MARKING_STATE' && sender.tab?.id) {
    const on = !!msg.active;
    chrome.action.setBadgeText({ tabId: sender.tab.id, text: on ? 'ON' : '' });
    chrome.action.setBadgeBackgroundColor({ tabId: sender.tab.id, color: '#3b82f6' });
    return;
  }

  if (msg?.type === 'CLICKMAP_SYNC_NOW') {
    syncPoisToBridge()
      .then((out) => sendResponse({ ok: true, out }))
      .catch((err) => sendResponse({ ok: false, error: err.message }));
    return true;
  }
});
