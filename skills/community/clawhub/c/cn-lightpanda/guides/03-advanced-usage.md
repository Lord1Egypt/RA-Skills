# 高级用法

## Playwright 集成

Playwright 通过 `connect` 方法连接到 Lightpanda 的 CDP 服务器：

```typescript
import { chromium } from 'playwright';

// 先启动 Lightpanda: ./lightpanda serve
const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');

const context = await browser.newContext();
const page = await context.newPage();

await page.goto('https://example.com');

// 等待元素并提取
await page.waitForSelector('.content');
const text = await page.textContent('.content');
console.log(text);

// 表单操作
await page.fill('#search', 'lightpanda');
await page.click('#submit');
await page.waitForLoadState('networkidle');

const results = await page.$$eval('.result', els => els.map(e => e.textContent));
console.log(results);

await context.close();
await browser.close();
```

---

## 代理配置

Lightpanda 支持 HTTP/SOCKS 代理：

```bash
# CLI 使用代理
./lightpanda fetch --dump markdown \
  --proxy http://user:pass@proxy.example.com:8080 \
  https://target-site.com

# 启动带代理的 CDP 服务器
./lightpanda serve \
  --proxy http://proxy.example.com:8080 \
  --host 127.0.0.1 \
  --port 9222
```

通过 Puppeteer 配置代理：

```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

// Puppeteer 可在页面级别设置代理认证
const page = await browser.newPage();
await page.authenticate({ username: 'user', password: 'pass' });
await page.goto('https://target-site.com');
```

---

## 自定义 HTTP 请求头

```bash
# 添加自定义请求头
./lightpanda fetch --dump html \
  --header "Authorization: Bearer token123" \
  --header "User-Agent: MyBot/1.0" \
  https://api.example.com
```

---

## 网络拦截（Puppeteer）

```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

const page = await browser.newPage();

// 开启请求拦截
await page.setRequestInterception(true);
page.on('request', request => {
  // 过滤图片和字体（加速爬取）
  if (['image', 'font', 'stylesheet'].includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});

await page.goto('https://news-site.com');
const articles = await page.$$eval('article h2', els => els.map(e => e.textContent));
console.log(articles);
```

---

## AI 智能体场景：批量页面爬取

Lightpanda 极低的内存占用使其非常适合 AI 智能体大规模爬取：

```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

// 并发爬取 50 个页面（Chrome 会 OOM，Lightpanda 轻松处理）
async function crawl(url) {
  const ctx = await browser.createBrowserContext();
  const page = await ctx.newPage();
  
  try {
    await page.goto(url, { timeout: 10000, waitUntil: 'networkidle0' });
    return await page.evaluate(() => ({
      title: document.title,
      text: document.body.innerText.slice(0, 500),
    }));
  } catch (e) {
    return { error: e.message, url };
  } finally {
    await page.close();
    await ctx.close();
  }
}

const urls = Array.from({ length: 50 }, (_, i) => `https://example.com/page/${i + 1}`);
const CONCURRENCY = 10;

// 批次并发处理
for (let i = 0; i < urls.length; i += CONCURRENCY) {
  const batch = urls.slice(i, i + CONCURRENCY);
  const results = await Promise.all(batch.map(crawl));
  results.forEach(r => console.log(r.title));
}

await browser.disconnect();
```

---

## Docker Compose 部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  lightpanda:
    image: lightpanda/browser:nightly
    ports:
      - "127.0.0.1:9222:9222"
    environment:
      - LIGHTPANDA_DISABLE_TELEMETRY=true
    restart: unless-stopped
    
  crawler:
    build: .
    environment:
      - BROWSER_WS=ws://lightpanda:9222
    depends_on:
      - lightpanda
```

---

## 从源码构建

仅在需要最新特性或定制修改时才需要从源码构建：

```bash
# 安装 Zig 0.15.2（必须是精确版本）
# 从 https://ziglang.org/download/ 下载

# 克隆仓库
git clone https://github.com/lightpanda-io/browser.git
cd browser

# 下载子依赖
./zig/download.sh

# 构建（耗时较长）
zig build -Doptimize=ReleaseFast

# 二进制位于 zig-out/bin/lightpanda
./zig-out/bin/lightpanda version
```

---

## 遥测控制

```bash
# 永久禁用（推荐生产环境）
echo 'export LIGHTPANDA_DISABLE_TELEMETRY=true' >> ~/.bashrc
source ~/.bashrc

# 单次禁用
LIGHTPANDA_DISABLE_TELEMETRY=true ./lightpanda serve
```

---

## 完成确认检查清单

- [ ] Playwright 脚本通过 `connectOverCDP` 成功连接并执行操作
- [ ] 代理配置后目标页面返回正确内容（可选）
- [ ] 高并发场景下内存稳定（对比 Headless Chrome 有明显改善）
- [ ] Docker Compose 部署正常（生产场景）

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [完整文档](https://lightpanda.io/docs)
- [MCP 服务器文档](https://lightpanda.io/docs/open-source/guides/mcp-server)
- [基准测试详情](https://github.com/lightpanda-io/demo/blob/main/BENCHMARKS.md)
