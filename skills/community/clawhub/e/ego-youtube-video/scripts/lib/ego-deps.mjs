import { LOGIN_COOKIE_RE, LOGIN_WALL_RE, PLATFORM_CHROME_RE, STUDIO_URL } from "./pure.mjs";
import { studioAct } from "./studio-dom.mjs";

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
          // Studio keeps sockets open.
        }
        await page.waitForTimeout(1200);
      };
      if (startUrl) await goto(startUrl);

      return {
        spaceId: task.spaceId,
        goto,
        url: () => page.url(),
        async detect() {
          const probed = await page.evaluate(studioAct, { op: "probe" });
          const url = probed.url || await page.url();
          const title = probed.title || await page.title();
          const text = probed.text || "";
          const blob = `${url}\n${title}\n${text}`;
          return {
            url,
            title,
            text,
            cookie: probed.cookie || "",
            platformChrome: PLATFORM_CHROME_RE.test(text),
            onLoginWall: LOGIN_WALL_RE.test(blob) || /accounts\.google\.com/i.test(url || "") || /\/signin/i.test(url || ""),
            loggedInCookie: LOGIN_COOKIE_RE.test(probed.cookie || ""),
          };
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

export { STUDIO_URL };
