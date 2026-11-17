// 后台 service worker：投递到用户配置的任意网盘通服务
async function getBase() { const d = await chrome.storage.local.get("serverUrl"); const u = (d.serverUrl || "").trim(); return u ? u.replace(/\/$/, "") : "http://127.0.0.1:17890"; }
// v0.19.0 起 Web API 启用 token 鉴权：在扩展选项里填入服务端 token
// （服务端启动横幅打印：pan serve → "带 token 入口"）
async function getAuthHeaders() {
  const d = await chrome.storage.local.get("apiToken");
  const t = (d.apiToken || "").trim();
  return t ? { "Authorization": "Bearer " + t } : {};
}
const MENU_ID = "pan-dl-send";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: MENU_ID,
      title: "发送 网盘链接 到 pan 下载",
      contexts: ["selection", "page", "link", "editable"]
    });
  });
});

async function loadDefaults() {
  const stored = await chrome.storage.local.get(["pwd", "to", "engine", "tier", "path"]);
  return {
    pwd: stored.pwd || "",
    to: stored.to || "",
    engine: stored.engine || "",
    tier: stored.tier || "",
    path: stored.path || ""
  };
}

function pickUrl(text) {
  const items = String(text || "").split(/\s+/).filter((s) => /^https?:\/\//i.test(s));
  return items[0] || "";
}

async function sendToPan(url, opts) {
  const body = { url: (url || "").trim() };
  if (opts.confirm_auth) body.confirm_auth = true;
  if (opts.source) body.source = opts.source;
  if (opts.pwd) body.pwd = opts.pwd;
  if (opts.to) body.to = opts.to;
  if (opts.engine) body.engine = opts.engine;
  if (opts.tier) body.tier = opts.tier;
  if (opts.path) body.path = opts.path;
  const resp = await fetch(await getBase() + "/api/download", {
    method: "POST",
    headers: Object.assign({ "Content-Type": "application/json" }, await getAuthHeaders()),
    body: JSON.stringify(body)
  });
  return await resp.json();
}

function notify(title, message) {
  try {
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icons/icon128.png",
      title: title,
      message: message
    });
  } catch (e) {
    console.log("notify failed", e);
  }
}

async function downloadFromText(text) {
  const url = pickUrl(text);
  if (!url) {
    notify("pan 下载", "未找到可用链接");
    return { ok: false, error: "no url" };
  }
  const opts = await loadDefaults();
  const data = await sendToPan(url, opts);
  if (!data.ok && data.login_required && data.login_url) {
    const target = new URL(data.login_url, await getBase()).toString();
    chrome.tabs.create({ url: target });
    notify("需要登录/授权", "已打开网盘通统一登录页");
    return data;
  }
  notify("pan 下载", data.ok ? "已开始：" + url : "失败：" + (data.error || "未知错误"));
  return data;
}

const recentCaptures = new Set();

chrome.downloads.onCreated.addListener(async (item) => {
  if (!item || !/^https?:\/\//i.test(item.url || "")) return;
  const state = await chrome.storage.local.get({ captureDownloads: true });
  if (!state.captureDownloads) return;
  const key = (item.url || "").split("#")[0];
  if (recentCaptures.has(key)) return;
  recentCaptures.add(key);
  setTimeout(() => recentCaptures.delete(key), 10 * 60 * 1000);
  const opts = await loadDefaults();
  const data = await sendToPan(item.url, { ...opts, confirm_auth: true, source: "browser-capture" });
  notify(data.ok ? "零客户端桥已接管" : "零客户端桥捕获失败", data.ok ? item.url : (data.error || "未知错误"));
});

chrome.contextMenus.onClicked.addListener(async (info) => {
  const text = info.linkUrl || info.selectionText || (info.menuItemId === MENU_ID ? (info.pageUrl || "") : "");
  await downloadFromText(text);
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "PAN_DOWNLOAD_URL") {
    (async () => {
      const data = await downloadFromText(msg.url || "");
      sendResponse(data);
    })();
    return true;
  }
  return false;
});
