// page.fetch session for x.com. Cookie values stay inside this process.

import { fetchPublicJs, isPublicClientWeb } from "./fetch-public.mjs";
import { loadClientWebBytes, readLoadedClientScript, warmClientScript } from "./loaded-script.mjs";
import { uploadImagesOnPage } from "./media-upload.mjs";
import { COMPOSE_URL, HOME_URL, cookieHeaderNames, detectSignals, parseLooseJson } from "./pure.mjs";
import {
  animationPathsFromHtml,
  buildTransactionId,
  describeMissingMaterials,
  onDemandFileUrl,
  shellHasMaterials,
} from "./transaction.mjs";

export async function readCookieJar(page) {
  if (!page || typeof page.cdp !== "function") return { cookies: [], read: false };
  try {
    const scoped = await page.cdp("Network.getCookies", { urls: ["https://x.com/", "https://twitter.com/"] });
    if (scoped && Array.isArray(scoped.cookies)) return { cookies: scoped.cookies, read: true };
  } catch {
    // Some ego builds want the unscoped call.
  }
  try {
    const all = await page.cdp("Network.getCookies");
    if (all && Array.isArray(all.cookies)) return { cookies: all.cookies, read: true };
  } catch {
    return { cookies: [], read: false };
  }
  return { cookies: [], read: false };
}

export function bodyText(raw) {
  if (typeof raw === "string") return raw;
  if (raw == null) return "";
  if (typeof Buffer !== "undefined" && Buffer.isBuffer(raw)) return raw.toString("utf8");
  if (raw instanceof Uint8Array) return new TextDecoder().decode(raw);
  return JSON.stringify(raw);
}

function cookieNames(jar, header) {
  return [
    ...cookieHeaderNames(header),
    ...(jar.cookies || []).map((cookie) => cookie && cookie.name).filter(Boolean),
  ];
}

export function createXSession({ task, page, pageName = "p1", keep = false, fetchPublicJs: loadPublic = fetchPublicJs } = {}) {
  if (!task || !page) throw new Error("createXSession requires task and page");
  let finished = false;
  const finishWith = async (names) => {
    if (finished) return;
    finished = true;
    await task.finish({ keep: names });
  };
  function loadClientWeb(url) {
    // Node and the Ego browser run together. Pro often cannot open
    // abs.twimg.com from Node; the browser warm-up still can. Mini's Node
    // path wins when it returns first, and the loser is aborted.
    return loadClientWebBytes({
      url,
      readCached: (target) => readLoadedClientScript(page, target),
      warm: (target, warmOptions) => warmClientScript(page, target, warmOptions),
      loadPublic: (target, fetchOptions) => loadPublic(target, fetchOptions),
    });
  }
  return {
    spaceId: task.spaceId,
    async goto(url) {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45_000 });
      try {
        if (typeof page.waitForLoadState === "function") await page.waitForLoadState("networkidle", { timeout: 8_000 });
      } catch {
        // x.com keeps sockets open after the shell is ready.
      }
      if (typeof page.waitForTimeout === "function") await page.waitForTimeout(800);
    },
    async ensureSite() {
      let current = "";
      try {
        current = await page.url();
      } catch {
        current = "";
      }
      if (!current || !/x\.com|twitter\.com/i.test(String(current))) await this.goto(HOME_URL);
    },
    async detect() {
      let url = "";
      let title = "";
      let probe = { text: "", href: "", cookie: "", lang: "" };
      try { url = await page.url(); } catch { url = ""; }
      try { title = await page.title(); } catch { title = ""; }
      try {
        const evaluated = await page.evaluate(() => {
          const text = (document.body && document.body.innerText) || "";
          const profile = document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
          let href = profile ? profile.getAttribute("href") || "" : "";
          if (!href) {
            const links = document.querySelectorAll("a[href]");
            for (const link of links) {
              const label = (link.innerText || "").trim();
              if (label === "个人资料" || label === "Profile") {
                href = link.getAttribute("href") || "";
                break;
              }
            }
          }
          return {
            text: text.slice(0, 4000),
            href,
            cookie: document.cookie || "",
            lang: (document.documentElement && document.documentElement.lang) || "",
          };
        });
        if (evaluated) probe = evaluated;
      } catch {
        // A blank tab still gets a cookie-jar read below.
      }
      const jar = await readCookieJar(page);
      const names = new Set(cookieNames(jar, probe.cookie));
      const signals = detectSignals({
        url,
        title,
        text: probe.text,
        profileHref: probe.href,
        authCookie: names.has("auth_token"),
        csrfCookie: names.has("ct0"),
        jarRead: jar.read,
      });
      return { url, title, text: probe.text || "", lang: probe.lang || "", ...signals };
    },
    async pageSource() {
      const html = await page.evaluate(() => (document.documentElement && document.documentElement.outerHTML) || "");
      return String(html || "");
    },
    fetchPublicJs: loadClientWeb,
    async fetchText(url, timeout = 30_000) {
      if (isPublicClientWeb(url)) {
        throw new Error("abs.twimg.com is fetched with Node, not page.fetch");
      }
      const response = await page.fetch(url, {
        method: "GET",
        credentials: "include",
        timeout,
      });
      return bodyText(response ? response.body : "");
    },
    async csrfToken() {
      let fromDoc = "";
      try {
        fromDoc = await page.evaluate(() => {
          const match = (document.cookie || "").match(/(?:^|;\s*)ct0=([^;]+)/);
          return match ? decodeURIComponent(match[1]) : "";
        });
      } catch {
        fromDoc = "";
      }
      if (fromDoc) return String(fromDoc);
      const jar = await readCookieJar(page);
      const ct0 = (jar.cookies || []).find((cookie) => cookie && cookie.name === "ct0" && cookie.value);
      return ct0 ? String(ct0.value) : "";
    },
    async animationPaths() {
      const paths = await page.evaluate(() => {
        return Array.from(document.querySelectorAll("[id^='loading-x-anim']")).map((frame) => {
          const group = frame.children && frame.children[0];
          const node = group && group.children && group.children[1];
          return node && node.getAttribute ? (node.getAttribute("d") || "") : "";
        });
      });
      return Array.isArray(paths) ? paths.map((path) => String(path || "")) : [];
    },
    async shellHtml() {
      if (this._shell) return this._shell;
      const urls = ["https://x.com/i/jf/", "https://x.com/home", "https://x.com/"];
      let best = "";
      for (const url of urls) {
        let text = "";
        try {
          text = await this.fetchText(url);
        } catch {
          text = "";
        }
        if (shellHasMaterials(text)) {
          this._shell = text;
          return text;
        }
        if (text && text.length > best.length) best = text;
      }
      try {
        await this.goto("https://x.com/i/jf/");
      } catch {
        // The fetched documents above are enough when they already contain the shell.
      }
      try {
        const live = await this.pageSource();
        if (shellHasMaterials(live)) {
          this._shell = live;
          return live;
        }
        if (live && live.length > best.length) best = live;
      } catch {
        // pageSource can fail when the DOM is too large to read back.
      }
      try {
        await this.goto(HOME_URL);
      } catch {
        // Stay where navigation left us; the POST does not depend on the visible tab.
      }
      this._shell = best;
      return best;
    },
    async scriptUrls() {
      try {
        const urls = await page.evaluate(() => {
          const out = [];
          const push = (value) => {
            if (typeof value !== "string" || !value.includes("abs.twimg.com/responsive-web/client-web/")) return;
            out.push(value.split("?")[0]);
          };
          for (const script of Array.from(document.scripts || [])) push(script.src);
          try {
            for (const entry of performance.getEntriesByType("resource")) push(entry.name);
          } catch {
            // performance is optional in older documents
          }
          return out;
        });
        return Array.isArray(urls) ? [...new Set(urls.map((url) => String(url)))] : [];
      } catch {
        return [];
      }
    },
    async paceCompose() {
      await this.goto(COMPOSE_URL);
      if (typeof page.waitForTimeout === "function") await page.waitForTimeout(2000);
    },
    async clientTransaction({ method, path } = {}) {
      const html = await this.shellHtml();
      let paths = animationPathsFromHtml(html);
      if (!paths.some(Boolean)) {
        try {
          paths = await this.animationPaths();
        } catch {
          paths = [];
        }
      }
      let liveOndemand = "";
      try {
        liveOndemand = (await this.scriptUrls()).find((url) => /\/ondemand\.s\.[A-Za-z0-9_-]+\.js$/.test(url)) || "";
      } catch {
        liveOndemand = "";
      }
      const chunkUrl = liveOndemand || onDemandFileUrl(html);
      let chunk = "";
      let fetchError = "";
      if (chunkUrl) {
        try {
          chunk = await loadClientWeb(chunkUrl);
        } catch (error) {
          fetchError = error && error.message ? error.message : "fetch failed";
          chunk = "";
        }
      }
      const id = await buildTransactionId({ method, path, html, ondemandSource: chunk, paths });
      if (id) return { id, source: "generated" };
      // A header sniffed from a different GraphQL call is bound to that path.
      // Pro accept2 reused one and CreateNoteTweet returned GraphQL 226.
      const missing = describeMissingMaterials({ html, ondemandSource: chunk, paths });
      const detail = [
        missing.join(", ") || "transaction materials",
        chunkUrl ? `ondemand bytes ${chunk.length}` : "no ondemand url",
        fetchError,
      ].filter(Boolean).join("; ");
      const error = new Error(`x.com document is missing ${detail}`);
      error.code = "TRANSACTION_MATERIALS";
      throw error;
    },
    async screenName() {
      const href = await page.evaluate(() => {
        const profile = document.querySelector('a[data-testid="AppTabBar_Profile_Link"]');
        if (profile) return profile.getAttribute("href") || "";
        const links = document.querySelectorAll("a[href]");
        for (const link of links) {
          const label = (link.innerText || "").trim();
          if (label === "个人资料" || label === "Profile") return link.getAttribute("href") || "";
        }
        return "";
      });
      return String(href || "");
    },
    async uploadImages(request) {
      return uploadImagesOnPage(page, request);
    },
    async postJson(request) {
      const response = await page.fetch(request.url, {
        method: "POST",
        credentials: "include",
        headers: request.headers,
        body: JSON.stringify(request.body),
        timeout: 30_000,
      });
      const raw = response ? response.body : undefined;
      const body = typeof raw === "string" || raw == null ? parseLooseJson(raw) : raw;
      return { status: response && response.status ? response.status : 0, body };
    },
    async handOff() {
      if (typeof task.handOff === "function") await task.handOff();
    },
    finish() {
      return finishWith(keep ? [pageName] : []);
    },
    cleanup() {
      return finishWith([]);
    },
  };
}
