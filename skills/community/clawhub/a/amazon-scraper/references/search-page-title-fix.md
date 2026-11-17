# 搜索页 `title: null` 根因 + 修复

## 现象

`amazon_handler.js` 跑 `/s?k=...` 搜索页时，**`title` 字段全部是 `null`**，但 `asin/price/rating/reviews/image/boughtPastMonth/sponsored` 都正常。

## 根因

Amazon 搜索页的 `<h2>` 元素是 **JS 动态加载**的。固定 `waitForTimeout(3000)` 不够长 — 第一次 3 秒内 h2 还没出现，handler 读到空 innerText。

**实证**（2026-07-02）：
- 等 3 秒：`h2 a span` 元素 = 0
- 等 8 秒：`h2 a span` 元素 = 34

handler 原来的 `await page.waitForTimeout(3000)` 在网络慢时永远等不够。

## 修复（已合入 v3.3.4.1 patched）

**位置**：`assets/amazon_handler.js` 第 153-160 行附近

```js
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
// Wait for search result cards (search pages need longer for JS-rendered titles)
if (pageType === 'search') {
    try {
        await page.waitForSelector('[data-component-type="s-search-result"]', { timeout: 15000 });
        // Wait until at least 10 cards have non-empty h2 text (Amazon lazy-renders titles)
        await page.waitForFunction(() => {
            const cards = document.querySelectorAll('[data-component-type="s-search-result"] h2 a span, [data-component-type="s-search-result"] h2 span');
            let nonEmpty = 0;
            for (const c of cards) { if (c.textContent.trim().length > 5) nonEmpty++; }
            return nonEmpty >= 10;
        }, { timeout: 20000 });
    } catch(e) { console.error('Search wait failed:', e.message); }
} else {
    await page.waitForTimeout(3000);
}
```

**title 选择器 fallback**（line 308）：

```js
// 原：单一选择器
const titleEl = card.querySelector('h2 a span');
// 改：双选择器 fallback
const titleEl = card.querySelector('h2 a span') || card.querySelector('h2 span');
```

## ⚠️ 改完必须重新 build 镜像

**关键**：handler.js 是**烘焙进 Docker 镜像**的，宿主目录改了不生效。改完必须：

```bash
cd ~/.openclaw/skills/amazon-scraper
docker build -t amazon-scraper .   # 重新 build，让 patch 进镜像
```

只改 `config/proxies.json` **不需要**重 build（proxies 是运行时读取）。

## 验证修复

```bash
docker run --rm -v /tmp/test:/data amazon-scraper \
  node assets/amazon_handler.js "https://www.amazon.com/s?k=cable+management" \
  --pages 1 --output /data/test.json

python3 -c "
import json
d = json.load(open('/tmp/test/test.json'))
ps = d.get('products', [])
with_title = [p for p in ps if p.get('title')]
print(f'{len(with_title)}/{len(ps)} have titles')
print(ps[0].get('title', '(none)')[:100])
"
```

期望输出：`20+/20+ have titles` + 第一个产品是真实标题（如 "Alex Tech 10ft - 1/2 inch Cord Protector..."）。

## Fallback（如果没改代码）

不需要重 build / 不影响现有镜像的情况下，可以用 **`vision_analyze` 看图识物**（参考 `product-form-fusion.md`）— 但这是"识别形态"路径，不是"拿 title 字段"。

## 经验教训

**Amazon 任何"动态渲染"页面（搜索/详情/评价）** — `waitForSelector` + `waitForFunction` 轮询"非空" 比固定 `waitForTimeout` 稳。前者自适应网络抖动，后者会随机翻车。
