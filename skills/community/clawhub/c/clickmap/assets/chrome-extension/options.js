const $ = (id) => document.getElementById(id);

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function sendToTab(msg) {
  const tab = await getActiveTab();
  if (!tab?.id) throw new Error('No active tab');
  return chrome.tabs.sendMessage(tab.id, msg);
}

function status(text) { $('status').textContent = text; }

function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1200);
}

function renderList() {
  chrome.storage.local.get(['clickmapPOIs'], (r) => {
    const pois = Array.isArray(r.clickmapPOIs) ? r.clickmapPOIs : [];
    const ul = $('list');
    ul.innerHTML = '';
    pois.forEach((p) => {
      const li = document.createElement('li');
      li.textContent = `${p.name} — ${p.urlPattern || '*'}`;
      ul.appendChild(li);
    });
    status(`POIs: ${pois.length}`);
  });
}

function loadBridge() {
  chrome.storage.local.get(['clickmapBridge'], (r) => {
    const bridge = r.clickmapBridge || { url: 'http://127.0.0.1:18795', token: '' };
    $('bridge').value = bridge.url || 'http://127.0.0.1:18795';
    $('token').value = bridge.token || '';
  });
}

function saveBridge() {
  const bridge = { url: $('bridge').value.trim(), token: $('token').value.trim() };
  chrome.storage.local.set({ clickmapBridge: bridge }, () => status('Bridge saved'));
}

$('saveBridge').onclick = saveBridge;

$('start').onclick = async () => {
  try { await sendToTab({ type: 'CLICKMAP_START' }); status('Marking mode ON'); } catch (e) { status(e.message); }
};
$('stop').onclick = async () => {
  try { await sendToTab({ type: 'CLICKMAP_STOP' }); status('Marking mode OFF'); } catch (e) { status(e.message); }
};

$('clear').onclick = () => {
  if (!confirm('Delete all saved POIs?')) return;
  chrome.storage.local.set({ clickmapPOIs: [] }, () => { renderList(); status('Cleared all POIs'); });
};

$('export').onclick = () => {
  chrome.storage.local.get(['clickmapPOIs'], (r) => {
    downloadJson('clickmap-pois.json', { version: 1, pois: r.clickmapPOIs || [] });
    status('Exported JSON');
  });
};

$('importBtn').onclick = () => $('file').click();
$('file').onchange = async (ev) => {
  const file = ev.target.files?.[0];
  if (!file) return;
  try {
    const data = JSON.parse(await file.text());
    const pois = Array.isArray(data.pois) ? data.pois : [];
    chrome.storage.local.set({ clickmapPOIs: pois }, () => { renderList(); status(`Imported ${pois.length} POIs`); });
  } catch {
    status('Invalid JSON file');
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
    } catch (e) {
      status(`Sync failed: ${e.message}`);
    }
  });
};

loadBridge();
renderList();
