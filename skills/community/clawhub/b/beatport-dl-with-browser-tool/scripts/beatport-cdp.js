const WS = require("/opt/homebrew/lib/node_modules/openclaw/node_modules/ws");
const http = require("http");
const fs = require("fs");

/**
 * Get a page from the CDP debugger
 */
function getPage(filterFn) {
  return new Promise((resolve, reject) => {
    http.get("http://127.0.0.1:9222/json", (res) => {
      let body = "";
      res.on("data", (c) => body += c);
      res.on("end", () => {
        const pages = JSON.parse(body).filter(p => p.type === "page");
        if (filterFn) {
          resolve(pages.find(filterFn) || pages[0]);
        } else {
          resolve(pages[0]);
        }
      });
    }).on("error", reject);
  });
}

/**
 * Get the browser-level WebSocket URL
 */
function getBrowserWs() {
  return new Promise((resolve, reject) => {
    http.get("http://127.0.0.1:9222/json/version", (res) => {
      let body = "";
      res.on("data", (c) => body += c);
      res.on("end", () => {
        const data = JSON.parse(body);
        resolve(data.webSocketDebuggerUrl);
      });
    }).on("error", reject);
  });
}

/**
 * Connect to a page's WebSocket
 */
function connectPage(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WS(wsUrl);
    ws.on("open", () => resolve(ws));
    ws.on("error", reject);
  });
}

/**
 * Run JavaScript in browser context and return the value
 */
function evalJs(ws, expression) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    const handler = (m) => {
      const d = JSON.parse(m.toString());
      if (d.id === id) {
        ws.removeListener("message", handler);
        if (d.result && d.result.type === "undefined") {
          resolve(null);
        } else if (d.result && d.result.value !== undefined) {
          resolve(d.result.value);
        } else if (d.result && d.result.type === "error") {
          reject(new Error(d.result.description || "Eval error"));
        } else {
          resolve(d.result);
        }
      }
    };
    ws.on("message", handler);
    ws.send(JSON.stringify({
      id,
      method: "Runtime.evaluate",
      params: { expression, returnByValue: true }
    }));
  });
}

/**
 * Navigate to a URL (using location.href for cross-domain support)
 */
function navigate(ws, url) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    const handler = (m) => {
      const d = JSON.parse(m.toString());
      if (d.id === id) {
        ws.removeListener("message", handler);
        resolve();
      }
    };
    ws.on("message", handler);
    ws.send(JSON.stringify({
      id,
      method: "Runtime.evaluate",
      params: { expression: `location.href = "${url}"` }
    }));
  });
}

/**
 * Wait for page load event
 */
function waitForLoad(ws, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    const handler = (m) => {
      const d = JSON.parse(m.toString());
      if (d.method === "Page.loadEventFired") {
        ws.removeListener("message", handler);
        resolve();
      }
    };
    ws.on("message", handler);
    setTimeout(() => {
      ws.removeListener("message", handler);
      reject(new Error("Timeout waiting for load"));
    }, timeoutMs);
  });
}

/**
 * Take a screenshot and save to file
 */
function screenshot(ws, path) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    const handler = (m) => {
      const d = JSON.parse(m.toString());
      if (d.id === id) {
        ws.removeListener("message", handler);
        if (d.result && d.result.data) {
          const buf = Buffer.from(d.result.data, "base64");
          fs.writeFileSync(path, buf);
          resolve(path);
        } else {
          reject(new Error("No screenshot data"));
        }
      }
    };
    ws.on("message", handler);
    ws.send(JSON.stringify({
      id,
      method: "Page.captureScreenshot",
      params: { format: "png" }
    }));
  });
}

/**
 * Enable downloads to a specific directory (browser-level)
 */
async function enableDownloads(downloadPath) {
  const browserWsUrl = await getBrowserWs();
  return new Promise((resolve, reject) => {
    const ws = new WS(browserWsUrl);
    ws.on("open", () => {
      ws.send(JSON.stringify({
        id: 1,
        method: "Browser.setDownloadBehavior",
        params: {
          behavior: "allowAndName",
          downloadPath: downloadPath,
          eventsEnabled: true
        }
      }));
    });
    ws.on("message", (m) => {
      const d = JSON.parse(m.toString());
      if (d.id === 1) {
        ws.close();
        resolve(d.result);
      }
    });
    ws.on("error", reject);
  });
}

/**
 * Get all cookies for a domain
 */
function getCookies(ws, urls) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    const handler = (m) => {
      const d = JSON.parse(m.toString());
      if (d.id === id) {
        ws.removeListener("message", handler);
        resolve(d.result.cookies);
      }
    };
    ws.on("message", handler);
    ws.send(JSON.stringify({
      id,
      method: "Network.getAllCookies",
      params: urls ? { urls } : {}
    }));
  });
}

/**
 * Login to Beatport via account.beatport.com
 */
async function login(ws, username, password) {
  // Navigate to login page
  await navigate(ws, "https://account.beatport.com/");
  await waitForLoad(ws);

  // Fill form using native input setter (bypasses React controlled inputs)
  await evalJs(ws, `
    var userInput = document.querySelector("input[name=username]") || document.querySelector("input[id=id_username]");
    if (userInput) {
      var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
      nativeSetter.call(userInput, "${username}");
      userInput.dispatchEvent(new Event("input", { bubbles: true }));
      userInput.dispatchEvent(new Event("change", { bubbles: true }));
    }
  `);

  await evalJs(ws, `
    var passInput = document.querySelector("input[name=password]") || document.querySelector("input[id=id_password]");
    if (passInput) {
      var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
      nativeSetter.call(passInput, "${password}");
      passInput.dispatchEvent(new Event("input", { bubbles: true }));
      passInput.dispatchEvent(new Event("change", { bubbles: true }));
    }
  `);

  // Submit
  await evalJs(ws, `
    var form = document.querySelector("form");
    if (form) form.submit();
  `);

  await waitForLoad(ws, 5000);
}

/**
 * Capture a download URL by clicking "Download All" and intercepting
 * the Page.downloadWillBegin event
 */
function captureDownloadUrl(ws) {
  return new Promise((resolve, reject) => {
    const id = Date.now();
    ws.send(JSON.stringify({ id: 0, method: "Page.enable" }));
    ws.send(JSON.stringify({ id: 1, method: "Page.setDownloadBehavior", params: { behavior: "deny" } }));

    const handler = (m) => {
      const d = JSON.parse(m.toString());
      if (d.method === "Page.downloadWillBegin") {
        ws.removeListener("message", handler);
        resolve(d.params.url);
      }
    };
    ws.on("message", handler);
  });
}

/**
 * Click "Download All" button on library/downloads page
 */
async function clickDownloadAll(ws) {
  await evalJs(ws, `
    var btn = [...document.querySelectorAll("button")].find(b => b.innerText.includes("Download All"));
    if (btn) btn.click();
    !!btn;
  `);
}

module.exports = {
  getPage, getBrowserWs, connectPage, evalJs, navigate,
  waitForLoad, screenshot, enableDownloads, getCookies, login,
  captureDownloadUrl, clickDownloadAll
};
