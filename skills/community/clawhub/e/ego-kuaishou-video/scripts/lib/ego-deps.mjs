import { BASE, LOGIN_COOKIE_RE, LOGIN_WALL_RE, PLATFORM_CHROME_RE, PUBLISH_URL } from "./pure.mjs";

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
          // The creator site keeps sockets open.
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
          const probe = await page.evaluate(() => {
            const text = (document.body && document.body.innerText) || "";
            return {
              text: text.slice(0, 4000),
              cookie: document.cookie || "",
            };
          });
          const blob = `${url}\n${title}\n${probe.text}`;
          return {
            url,
            title,
            text: probe.text,
            platformChrome: PLATFORM_CHROME_RE.test(probe.text),
            onLoginWall: LOGIN_WALL_RE.test(blob) || /\/login/i.test(url || ""),
            loggedInCookie: LOGIN_COOKIE_RE.test(probe.cookie || ""),
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

export { BASE, PUBLISH_URL };
