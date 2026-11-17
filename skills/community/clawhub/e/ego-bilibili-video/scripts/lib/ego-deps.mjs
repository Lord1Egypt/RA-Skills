import { BASE, FRAME_URL } from "./pure.mjs";

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
          // member.bilibili.com keeps sockets open
        }
        await page.waitForTimeout(1500);
      };
      if (startUrl) await goto(startUrl);

      return {
        spaceId: task.spaceId,
        goto,
        url: () => page.url(),
        // B 站创作中心是 micro-app + shadow DOM,正文探测要走 shadow walk。
        async probe() {
          const url = await page.url();
          const data = await page.evaluate(() => {
            function* walk(root) {
              for (const el of root.querySelectorAll("*")) {
                if (el.shadowRoot) yield* walk(el.shadowRoot);
                yield el;
              }
            }
            let shadowText = "";
            for (const el of walk(document)) {
              const own = [...el.childNodes]
                .filter((n) => n.nodeType === 3)
                .map((n) => n.textContent.trim())
                .join("");
              if (own) shadowText += `${own}\n`;
              if (shadowText.length > 4000) break;
            }
            return { shadowText: shadowText.slice(0, 4000), bodyText: (document.body.innerText || "").slice(0, 4000) };
          });
          return { url, text: `${data.bodyText}\n${data.shadowText}` };
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

export { BASE, FRAME_URL };
