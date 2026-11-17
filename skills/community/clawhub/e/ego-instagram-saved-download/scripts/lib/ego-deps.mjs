import { browserSave, fetchMediaBytes, requestBytes } from "./media-fetch.mjs";
import { BASE, WEB_APP_ID, bufferFetchResponse } from "./pure.mjs";

const UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36";

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
          // Instagram keeps background requests open.
        }
        await page.waitForTimeout(1200);
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
              password: Boolean(document.querySelector('input[type="password"]')),
              username: Boolean(document.querySelector('input[name="username"]')),
              inbox: Boolean(document.querySelector('a[href*="/direct/inbox"]')),
              saved: Boolean(document.querySelector('a[href*="/saved"]')),
              dsUser: /(?:^|;\s*)ds_user_id=/.test(cookie),
            };
          });
          return { url, title, ...flags };
        },
        async fetchJson(apiPath) {
          const token = await page.evaluate(() => {
            const match = (document.cookie || "").match(/(?:^|;\s*)csrftoken=([^;]+)/);
            return match ? match[1] : "";
          });
          const response = await page.fetch(apiPath, {
            method: "GET",
            headers: {
              Accept: "*/*",
              "X-Requested-With": "XMLHttpRequest",
              "X-IG-App-ID": WEB_APP_ID,
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
              if (!value || typeof value !== "string" || !/cdninstagram\.com|fbcdn\.net/i.test(value)) return;
              const clean = value.split("?")[0];
              if (seen.has(clean)) return;
              seen.add(clean);
              urls.push(clean);
            };
            for (const img of document.querySelectorAll("img")) push(img.currentSrc || img.src);
            return urls.slice(0, Math.max(max, 1));
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
