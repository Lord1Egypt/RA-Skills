import { BASE, HOME_URL, SPACE_NAME, detectSignals, loggedInCookieHeader } from "./pure.mjs";
import { createPageSession } from "./session.mjs";

function defaultTaskSpace(name) {
  const open = globalThis.taskSpace;
  if (typeof open !== "function") {
    throw new Error("taskSpace is only available inside ego-browser nodejs");
  }
  return open(name);
}

export async function readCookieJar(page) {
  if (!page || typeof page.cdp !== "function") return [];
  try {
    const scoped = await page.cdp("Network.getCookies", { urls: [HOME_URL] });
    if (scoped && Array.isArray(scoped.cookies)) return scoped.cookies;
  } catch {
    // Some ego builds want the unscoped call.
  }
  try {
    const all = await page.cdp("Network.getCookies");
    return all && Array.isArray(all.cookies) ? all.cookies : [];
  } catch {
    return [];
  }
}

export function createEgoBrowser({ taskSpace: openSpace = defaultTaskSpace } = {}) {
  return {
    async open({ taskName, startUrl, keepBrowser }) {
      const task = await openSpace(taskName);
      const page = task.page("p1");
      let finished = false;
      const goto = async (url) => {
        await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45_000 });
        try {
          await page.waitForLoadState("networkidle", { timeout: 8_000 });
        } catch {
          // Teambition keeps sockets open after the shell is ready.
        }
        if (typeof page.waitForTimeout === "function") await page.waitForTimeout(800);
      };
      if (startUrl) await goto(startUrl);

      return {
        spaceId: task.spaceId,
        goto,
        url: () => page.url(),
        async detect() {
          const url = await page.url();
          const title = await page.title();
          const probe = await page.evaluate(() => {
            const text = (document.body && document.body.innerText) || "";
            return {
              text: text.slice(0, 4000),
              cookie: document.cookie || "",
            };
          });
          const jar = await readCookieJar(page);
          const cookie = [probe.cookie, loggedInCookieHeader(jar)].filter(Boolean).join("; ");
          const signals = detectSignals({ url, title, text: probe.text, cookie });
          return { url, title, text: probe.text, ...signals };
        },
        async finish() {
          if (finished) return;
          finished = true;
          await task.finish({ keep: keepBrowser ? ["p1"] : [] });
        },
        async handOff() {
          await task.handOff();
        },
      };
    },
  };
}

export async function createEgoSession(config = {}, deps = {}) {
  const openSpace = deps.taskSpace || defaultTaskSpace;
  const task = await openSpace(config.taskName || SPACE_NAME);
  const page = task.page(config.pageName || "p1");
  return createPageSession({
    task,
    page,
    base: BASE,
    pageName: config.pageName || "p1",
  });
}
