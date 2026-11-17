import { BASE } from "./pure.mjs";

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
          // Channels keeps sockets open.
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
            const cookie = document.cookie || "";
            return {
              text: text.slice(0, 4000),
              platformChrome: /内容管理|发表视频|草稿箱/.test(text),
              loggedInCookie: /(?:^|;\s*)(sessionid|wxuin|uin)=/i.test(cookie),
            };
          });
          return { url, title, ...probe };
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

export { BASE };
