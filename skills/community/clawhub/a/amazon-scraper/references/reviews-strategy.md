# Amazon Reviews 抓取策略

> ## ⚠️ 先读这段：这条路线的代价和别的不一样
>
> 榜单 / 搜索 / 详情页是匿名可见的公开页面，抓取成本只是代理费。**评论页要求真实买家登录态**，性质完全不同：
>
> - **账号风险**：抓取行为绑定到一个真实账号上。被判定自动化访问时封的是这个账号，连带历史订单、Prime、礼品卡余额；如果它和卖家账号有关联信息，可能牵连卖家账号。用专用账号，不要用主账号、更不要用卖家关联账号。
> - **登录态即凭证**：导出的 cookie 文件和 CDP 调试口都等价于账号密码，必须按密钥对待（`chmod 600`、不放 `/tmp`、不进 git、不打包分享）。
> - **个人数据**：评论正文 + 作者名是第三方个人数据。落库就意味着你在处理个人信息（GDPR/CCPA 口径），应当只存分析真正需要的字段、设定保留期限并定期清理，而不是无限期全量留存。
> - 下面"CAPTCHA → 换 IP 换账号"是历史记录里的做法。**批量换账号绕验证码属于规避访问控制**，风险和合规代价都显著高于前面几种模式，不要当作常规手段。
>
> 结论：能用匿名页面拿到的字段就别走这条路；真要抓评论，先把上面四条的代价算清楚。

## 核心结论

Amazon 评论页（`/product-reviews/ASIN`）的反爬比 BSR/搜索页**严格得多**。匿名访问翻 2-3 页就弹 CAPTCHA 或返回空结果。**必须用已登录的 Amazon 买家账号 session**。

## 两种技术路线对比

| | Playwright+Stealth+代理（amazon-scraper 现有路线） | Chrome+CDP+已登录 session（amazon-alexa-shopping-qa 路线） |
|---|---|---|
| 适用页面 | BSR、搜索结果、产品详情（匿名可看） | 评论页、Alexa AI 对话（需登录） |
| 登录态 | 无 | ✅ 真实买家 Cookie |
| 浏览器指纹 | Stealth 模拟 | 真实 Chrome 指纹 |
| 代理认证 | Playwright 原生支持 `proxy: {username, password}` | Chrome `--proxy-server` 不支持用户名密码 → 需本地转发或用 Playwright |
| 反检测强度 | 中（Stealth 绕 headless） | 高（真实浏览器 + 登录态） |

## 方案 A：CDP 直连 Page WS（轻量，已验证 2026-07）

比 Playwright 更轻量：直接用 Chrome CDP WebSocket 操作已登录的页面。**必须连 page 级 WS，不能连 browser 级**。

### 关键坑：browser WS vs page WS

```
❌ ws://127.0.0.1:9222/devtools/browser/<id>  → Target.getTargets 能拿到列表，
   但 Runtime.evaluate 在 browser 级执行，找不到页面 DOM 元素
✅ ws://127.0.0.1:9222/devtools/page/<id>     → 直接操作页面 DOM，一切正常
```

获取 page WS URL：
```python
import json, urllib.request
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json').read())
page = [t for t in tabs if t['type']=='page' and 'amazon' in t.get('url','')][0]
ws_url = page['webSocketDebuggerUrl']
```

### Chrome 启动（必须加 --no-first-run）

```bash
PROFILE="$HOME/.cache/amazon-scraper-chrome"
mkdir -p "$PROFILE" && chmod 700 "$PROFILE"
# 清理上次崩溃的锁文件
rm -f "$PROFILE"/Singleton{Lock,Socket,Cookie}

Xvfb :99 -screen 0 1536x900x24 &
DISPLAY=:99 google-chrome \
  --disable-gpu \
  --no-first-run --no-default-browser-check \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$PROFILE" \
  "https://www.amazon.com" &
```

> ⚠️ 这个 Chrome 带着真实买家登录态，**它的 9222 调试口等于账号凭证**：CDP 无认证，连上即完全接管（读 cookie、下单、改地址）。所以：
> - 显式绑 `127.0.0.1`，别让它监听 `0.0.0.0`（`ss -lntp | grep 9222` 自查）
> - **不要加 `--remote-allow-origins=*`** —— 那会让这个浏览器里打开的任意网页都能接管它
> - 不要用 `--no-sandbox`（VPS 上通常是 root，等于把渲染器漏洞直接升级成 root）
> - profile 不要放 `/tmp`（全局可写，cookie 会被同机其他用户读到）
> - 抓完就关，别长期挂着

### 完整评论抓取脚本（CDP page WS 版）

```python
import json, urllib.request, websockets, asyncio

async def scrape_reviews(asin, target=10):
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json').read())
    page = [t for t in tabs if t['type']=='page' and 'amazon' in t.get('url','')][0]
    ws_url = page['webSocketDebuggerUrl']

    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        mid = 0
        async def cdp(method, params={}):
            nonlocal mid
            mid += 1
            await ws.send(json.dumps({"id": mid, "method": method, "params": params}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == mid:
                    return resp.get("result", {})

        async def eval_js(expr):
            r = await cdp("Runtime.evaluate", {
                "expression": expr, "returnByValue": True, "awaitPromise": True
            })
            return r.get("result", {}).get("value")

        await cdp("Page.navigate", {"url": f"https://www.amazon.com/product-reviews/{asin}/?pageNumber=1"})
        await asyncio.sleep(5)

        # 滚到底部触发懒加载
        await eval_js("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)

        # 提取完整评论 — innerText 已返回全文，无需展开
        reviews = await eval_js("""
            (function() {
                const items = document.querySelectorAll('[data-hook="review"]');
                return Array.from(items).map(r => {
                    const bodyEl = r.querySelector('[data-hook="review-body"] span')
                        || r.querySelector('[data-hook="review-body"]');
                    return {
                        rating: r.querySelector('[data-hook="review-star-rating"]')?.innerText?.trim() || '',
                        title: r.querySelector('[data-hook="review-title"]')?.innerText?.trim() || '',
                        body: bodyEl?.innerText?.trim() || '',
                        date: r.querySelector('[data-hook="review-date"]')?.innerText?.trim() || '',
                        helpful: r.querySelector('[data-hook="helpful-vote-statement"]')?.innerText?.trim() || '',
                        verified: !!r.querySelector('[data-hook="avp-badge"]')
                    };
                });
            })()
        """) or []

        return reviews[:target]
```

### 重要发现（2026-07 实战）

1. **`innerText` 已返回完整评论正文**（无折叠/截断）。之前出现的截断是脚本里 `[:200]` 人为截断的，不是 Amazon 限制
2. **title 字段包含评分前缀**：如 `"5.0 out of 5 stars\n Tamed My Cable Chaos"`，需清理
3. **Amazon 不折叠长评论**：`[data-hook="review-body"] span` 的 `innerText` 就是全文

## 方案 B：Playwright + Cookie 注入（可带代理）

用 amazon-scraper 的 Playwright + Stealth + 代理轮换做底盘，注入已登录的 Amazon Cookie：

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

const browser = await chromium.launch({
    headless: false,  // 或用 Xvfb
    proxy: {
        server: 'http://isp.oxylabs.io:8001',
        username: 'user-xxx',
        password: 'pass'
    }
});

const context = await browser.newContext({
    storageState: '$HOME/.cache/amazon-scraper-chrome/amazon-cookies.json'  // 已登录的 Cookie
});

const page = await context.newPage();

for (let pageNum = 1; pageNum <= 10; pageNum++) {
    await page.goto(
        `https://www.amazon.com/product-reviews/ASIN/?pageNumber=${pageNum}&pageSize=50`,
        { waitUntil: 'domcontentloaded' }
    );
    await page.waitForTimeout(2500);

    const reviews = await page.evaluate(() => {
        const items = document.querySelectorAll('[data-hook="review"]');
        return Array.from(items).map(r => ({
            rating: r.querySelector('[data-hook="review-star-rating"]')?.innerText,
            title: r.querySelector('[data-hook="review-title"]')?.innerText,
            body: r.querySelector('[data-hook="review-body"] span')?.innerText,
            date: r.querySelector('[data-hook="review-date"]')?.innerText,
            helpful: r.querySelector('[data-hook="helpful-vote-statement"]')?.innerText,
            verified: !!r.querySelector('[data-hook="avp-badge"]')
        }));
    });

    if (reviews.length === 0) break;
    allReviews.push(...reviews);
}
```

### Cookie 获取方法

从 amazon-alexa-shopping-qa 环境的 Chrome profile 导出：

```bash
# 1. 启动已登录的 Chrome
DISPLAY=:99 google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.cache/amazon-scraper-chrome" &

# 2. 用 CDP 导出 Cookie
python3 -c "
import asyncio, json, websockets, sys

async def get_cookies():
    ws_url = sys.argv[1]
    async with websockets.connect(ws_url) as ws:
        msg_id = 0
        msg_id += 1
        await ws.send(json.dumps({'id': msg_id, 'method': 'Storage.getCookies'}))
        resp = json.loads(await ws.recv())
        cookies = resp.get('result', {}).get('cookies', [])
        state = {'cookies': cookies, 'origins': []}
        with open('$HOME/.cache/amazon-scraper-chrome/amazon-cookies.json', 'w') as f:
            json.dump(state, f)
        print(f'导出 {len(cookies)} 个 Cookie')

asyncio.run(get_cookies())
" "ws://127.0.0.1:9222/devtools/browser/..."
```

## 评论量上限与分批策略

| 评论总量 | 能拿到多少 | 方法 |
|---|---|---|
| 几百条 | 全部 | 直接翻页 |
| 1-2千条 | 全部 | 真人节奏 + 代理轮换 |
| 5千+ | ~5000 条 | Amazon 硬上限（500页×10条） |
| 上万条 | ~25000 条 | 按星级分批（5个星级各自独立翻页） |

按星级分批 URL：`https://www.amazon.com/product-reviews/{asin}/?filterByStar=five_star&pageNumber={page}&pageSize=50`

## 关键注意事项

1. **用 `.click()` 翻页**，不要拼 URL — 更像真人操作
2. **每页间隔 2-3 秒**，每 5-10 个 ASIN 换一个代理端口
3. **代理必须用 ISP/Residential**，Datacenter 代理对 Amazon 评论页会被风控
4. **单 IP 一天别超过 30-50 个 ASIN** 的评论
5. **登录态会过期** — Amazon session 大约 2-4 周需要重新登录
6. **评论页选择器**（2026-07 验证）：
   - 评论容器：`[data-hook="review"]`
   - 评分：`[data-hook="review-star-rating"]`
   - 标题：`[data-hook="review-title"]`
   - 正文：`[data-hook="review-body"] span`
   - 日期：`[data-hook="review-date"]`
   - 有用投票：`[data-hook="helpful-vote-statement"]`
   - 已购买验证：`[data-hook="avp-badge"]`

## 翻页策略（2026-07 更新：瀑布流模式）

### ⚠️ Amazon 评论页已改为瀑布流

旧版 `/product-reviews/ASIN` 页面的传统分页（`.a-pagination` 翻页）**已失效**。现在 Amazon 用 `/portal/customer-reviews/ASIN` 页面 + **"Show 10 more reviews" 按钮**做无限滚动加载。

| 旧方式（已失效） | 新方式（当前可用） |
|---|---|
| `/product-reviews/ASIN?pageNumber=2` | `/portal/customer-reviews/ASIN` + 点按钮 |
| `.a-pagination li:last-child a` 翻页 | `.cm-cr-show-more a` 点击加载 |
| 每页 10 条，URL 变化 | 每次加载 10 条，URL 不变，DOM 追加 |
| 可按星级筛选分批 | 星级筛选待验证 |

### 正确的瀑布流抓取流程

1. 导航到 `https://www.amazon.com/portal/customer-reviews/{ASIN}`
2. 等 5-6 秒页面加载
3. `window.scrollTo(0, document.body.scrollHeight)` 滚到底部
4. 提取当前所有 `[data-hook="review"]`（全量提取，去重）
5. 点击 `.cm-cr-show-more a`（精确 selector，不要用文本匹配）
6. 等 2 秒让 AJAX 加载
7. 回到步骤 3，循环直到目标数量或按钮消失

### 关键坑

1. **必须连 page 级 WS**，不能连 browser 级（browser 级 `Runtime.evaluate` 找不到 DOM）
2. **按钮 selector 用 `.cm-cr-show-more a`**，不要用文本匹配 `"Show 10 more reviews"`（有多个重叠 DOM 元素，点错无效）
3. **按钮可能在视口外**（`y: -1869`），必须先 `scrollTo` 底部再点击
4. **点击后 1 秒就加载完成**，不需要等太久
5. **旧脚本超时原因**：用文本匹配点击了错误的 `<span>` 元素（有 3 层嵌套），实际可点击的是最内层 `<a class="a-button-text">`
6. **innerText 已返回完整正文**，无折叠/截断（之前 `[:200]` 是脚本人为截断）
7. **SQLite 写入时如果改了表结构**（如 `page` → `batch`），必须先 `DROP TABLE` 重建，否则 `OperationalError: table has no column named batch`

### 安全退出条件

- 连续 5 次点击无新增评论 → 退出
- 按钮消失（`.cm-cr-show-more a` 不存在）→ 退出
- 达到目标数量 → 退出

### CAPTCHA 处理

- CAPTCHA 出现 → 暂停 30 分钟 + 换 IP + 换账号
- 单 IP 一天别超过 30-50 个 ASIN 的评论

## 与 amazon-scraper 现有架构的关系

amazon-scraper 的 Docker 镜像已内置 Playwright + Stealth + 代理轮换。抓评论只需：
1. 加载已登录 Cookie（`storageState`）
2. 导航到 `/product-reviews/ASIN` 而不是 BSR/搜索页
3. 用 `.click()` 翻页 + 真人节奏等待

不需要新建 Docker 镜像，在现有 `amazon_handler.js` 里加一个 `reviews` 模式即可。
