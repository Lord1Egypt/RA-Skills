function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}
function randomDelay(min = 1000, max = 3000) {
    return Math.floor(Math.random() * (max - min) + min);
}
export async function fetchUrlContent(browser, url) {
    const page = await browser.newPage();
    try {
        await page.goto(url, { waitUntil: "domcontentloaded" });
        await page.evaluate(() => { window.scrollBy(0, 400); });
        await sleep(randomDelay());
        const data = await page.evaluate(() => {
            function getDomContent(s) {
                return document.querySelector(s)?.textContent?.trim() || "";
            }
            let title = getDomContent("#activity-name");
            if (!title) {
                title = getDomContent(".rich_media_title");
            }
            return title;
        });
        return data;
    }
    catch (e) {
        console.error("获取url内容失败:", e);
        return null;
    }
    finally {
        await page.close();
    }
}
//# sourceMappingURL=fetch-content.js.map