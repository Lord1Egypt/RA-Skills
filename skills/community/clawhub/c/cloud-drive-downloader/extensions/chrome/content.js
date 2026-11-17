// 内容脚本：监听复制/选择，把链接发送给后台 service worker
(() => {
  const MAX_QUEUE = 12;
  let lastSent = 0;

  function extractUrls(text) {
    if (!text) return [];
    const items = text.split(/\s+/).filter((s) => /^https?:\/\//i.test(s));
    return items.slice(0, MAX_QUEUE);
  }

  function sendUrls(text, source) {
    if (!text || typeof text !== "string") return;
    const urls = extractUrls(text);
    if (urls.length === 0) return;
    const now = Date.now();
    if (now - lastSent < 1500 && source === "copy") return; // 防止同一次复制重复触发
    lastSent = now;
    chrome.runtime.sendMessage({ type: "PAN_DOWNLOAD_URL", url: urls[0], urls: urls, source: source || "copy" });
  }

  // 复制事件：读取剪贴板文本中的链接
  document.addEventListener("copy", (e) => {
    try {
      const text = (e.clipboardData || window.clipboardData).getData("text/plain") || "";
      sendUrls(text, "copy");
    } catch (err) {
      console.warn("pan content copy", err);
    }
  });

  // 键盘复制（Ctrl/Cmd+C）：兜底读取当前选区
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && (e.key === "c" || e.key === "C")) {
      setTimeout(() => {
        try {
          const text = window.getSelection ? window.getSelection().toString() : "";
          sendUrls(text, "keyboard");
        } catch (err) {
          console.warn("pan content keydown", err);
        }
      }, 0);
    }
  });

  // 选区包含链接：交给后台（不读取登录态，只取浏览器选中文本）
  document.addEventListener("selectionchange", () => {
    try {
      const sel = window.getSelection ? window.getSelection().toString() : "";
      if (sel && /^https?:\/\/\S+/i.test(sel.trim())) {
        sendUrls(sel, "selection");
      }
    } catch (err) {
      console.warn("pan content selection", err);
    }
  });
})();
