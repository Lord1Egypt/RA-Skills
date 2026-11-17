import { browserSave, fetchMediaBytes, requestBytes } from "./media-fetch.mjs";
import { BASE, UA, bufferFetchResponse } from "./pure.mjs";

export function createEgoBrowser() {
  return {
    async open({ taskName, startUrl, keepBrowser }) {
      const task = await taskSpace(taskName);
      const page = task.page("p1");
      let finished = false;
      const goto = async (url) => {
        await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45_000 });
        try {
          await page.waitForLoadState("networkidle", { timeout: 8_000 });
        } catch {
          // Pinterest keeps background requests open.
        }
        await page.waitForTimeout(1000);
      };
      if (startUrl) await goto(startUrl);

      return {
        spaceId: task.spaceId,
        goto,
        url: () => page.url(),
        async detect() {
          const url = await page.url();
          const title = await page.title();
          const flags = await page.evaluate(() => {
            const cookie = document.cookie || "";
            return {
              unauth: Boolean(
                document.querySelector('[data-test-id="unauth-header"], [data-test-id="simple-login-button"]'),
              ),
              profile: Boolean(
                document.querySelector(
                  '[data-test-id="header-profile"], [data-test-id="header-accounts-options-button"], [data-test-id="header-avatar"], [data-test-id="business-account-switcher"]',
                ),
              ),
              authCookie: /(?:^|;\s*)_auth=1(?:;|$)/.test(cookie),
            };
          });
          return { url, title, ...flags };
        },
        async fetchJson(apiPath, extraHeaders = {}) {
          const token = await page.evaluate(() => {
            const match = (document.cookie || "").match(/(?:^|;\s*)csrftoken=([^;]+)/);
            return match ? match[1] : "";
          });
          const response = await page.fetch(apiPath, {
            method: "GET",
            headers: {
              Accept: "application/json, text/javascript, */*; q=0.01",
              "X-Requested-With": "XMLHttpRequest",
              "X-Pinterest-AppState": "active",
              ...extraHeaders,
              ...(token ? { "X-CSRFToken": token } : {}),
            },
            timeout: 20_000,
          });
          return { ok: response.ok, status: response.status, body: response.body };
        },
        async domImages(limit) {
          return page.evaluate((max) => {
            const urls = [];
            const seen = new Set();
            const push = (value) => {
              if (!value || typeof value !== "string" || !/pinimg\.com/i.test(value)) return;
              const clean = value.split("?")[0];
              if (seen.has(clean)) return;
              seen.add(clean);
              urls.push(clean);
            };
            for (const img of document.querySelectorAll("img")) {
              push(img.currentSrc || img.src);
              for (const part of (img.getAttribute("srcset") || "").split(",")) push(part.trim().split(/\s+/)[0]);
            }
            return urls.slice(0, Math.max(max * 3, 12));
          }, limit);
        },
        async fetchBytes(targetUrl, { maxBytes } = {}) {
          const headers = { "User-Agent": UA, Referer: `${BASE}/`, Accept: "*/*" };
          const referer = `${BASE}/`;
          return fetchMediaBytes({
            url: targetUrl,
            maxBytes,
            headers,
            nodeFetch: async (url, options) => {
              const response = await fetch(url, { headers: options.headers, redirect: "follow" });
              return bufferFetchResponse(response, options.maxBytes);
            },
            directFetch: (url, options) => requestBytes(url, { ...options, family: 4 }),
            browserFetch: (url, options) => browserSave(page, url, { ...options, referer }),
          });
        },
        async finish() {
          if (finished) return;
          finished = true;
          await task.finish({ keep: keepBrowser ? ["p1"] : [] });
        },
      };
    },
  };
}
