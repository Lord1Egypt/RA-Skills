# 快速开始

## 适用场景

- 将网页内容转储为 HTML 或 Markdown
- 启动 CDP 服务器，连接 Puppeteer/Playwright 脚本
- 配置 Lightpanda 作为 AI 工具的 MCP 服务器
- 替换现有 Headless Chrome 节省资源

---

## 命令行转储页面内容

最快的使用方式，无需写代码：

```bash
# 转储页面 HTML
./lightpanda fetch https://example.com --dump html

# 转储为 Markdown（AI 友好格式）
./lightpanda fetch --dump markdown https://news.ycombinator.com

# 等待页面动态加载后再转储
./lightpanda fetch --dump markdown \
  --wait-until networkidle \
  https://spa-app.com

# 等待特定元素出现后转储
./lightpanda fetch --dump html \
  --wait-selector "#content-loaded" \
  https://dynamic-app.com

# 等待固定时间（毫秒）
./lightpanda fetch --dump markdown \
  --wait-ms 2000 \
  https://slow-site.com

# 遵守 robots.txt
./lightpanda fetch --dump markdown \
  --obey-robots \
  https://example.com
```

---

## 启动 CDP 服务器

启动后即可被 Puppeteer/Playwright 连接：

```bash
# 默认配置（127.0.0.1:9222）
./lightpanda serve

# 指定端口
./lightpanda serve --host 127.0.0.1 --port 9222

# 带日志
./lightpanda serve \
  --log-format pretty \
  --log-level info \
  --host 127.0.0.1 \
  --port 9222

# Docker 方式
docker run -d --name lightpanda \
  -p 127.0.0.1:9222:9222 \
  lightpanda/browser:nightly
```

验证服务器就绪：
```bash
curl http://127.0.0.1:9222/json/version
# 期望返回: {"Browser":"lightpanda/...","webSocketDebuggerUrl":"ws://..."}
```

---

## Puppeteer 集成（零代码改动）

将现有 Puppeteer 脚本的 `browserWSEndpoint` 指向 Lightpanda：

```javascript
import puppeteer from 'puppeteer-core';

// 连接到 Lightpanda CDP 服务器
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

const context = await browser.createBrowserContext();
const page = await context.newPage();

// 以下代码与使用 Headless Chrome 完全相同
await page.goto('https://example.com', { waitUntil: "networkidle0" });

const title = await page.title();
console.log('Page title:', title);

// 提取所有链接
const links = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('a'))
    .map(a => a.getAttribute('href'));
});

console.log('Links:', links);

await page.close();
await context.close();
await browser.disconnect();
```

---

## 大规模爬取示例

```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:9222",
});

// 并发爬取多个页面
async function crawlPage(url) {
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "networkidle0" });
  const content = await page.evaluate(() => document.body.innerText);
  await page.close();
  await context.close();
  return content;
}

const urls = ['https://page1.com', 'https://page2.com', 'https://page3.com'];
// Lightpanda 极低内存占用，支持高并发
const results = await Promise.all(urls.map(crawlPage));
console.log(results);

await browser.disconnect();
```

---

## MCP 服务器配置

让 Claude/Cursor 等 AI 工具直接控制 Lightpanda 浏览器：

```bash
# 直接启动 MCP 服务器
./lightpanda mcp
```

### Claude Code 配置

```bash
# 获取 lightpanda 路径
which lightpanda
# 或: $(pwd)/lightpanda

# 添加到 Claude Code MCP
claude mcp add lightpanda --scope user /usr/local/bin/lightpanda mcp
```

### 手动 JSON 配置

```json
{
  "mcpServers": {
    "lightpanda": {
      "command": "/usr/local/bin/lightpanda",
      "args": ["mcp"]
    }
  }
}
```

### 在 AI 对话中使用

```
请用 Lightpanda 打开 https://news.ycombinator.com 并提取所有文章标题

请访问 https://example.com/products，等待商品列表加载完成，然后提取所有商品名称和价格
```

---

## 禁用遥测

Lightpanda 默认收集使用统计，禁用方式：

```bash
export LIGHTPANDA_DISABLE_TELEMETRY=true
./lightpanda serve
```

---

## 完成确认检查清单

- [ ] `./lightpanda fetch --dump markdown https://example.com` 返回页面内容
- [ ] `./lightpanda serve` 启动后 `curl http://127.0.0.1:9222/json/version` 返回 JSON
- [ ] Puppeteer 脚本通过 `browserWSEndpoint` 成功连接
- [ ] MCP 服务器启动（可选）

---

## 下一步

- [高级用法](03-advanced-usage.md) — Playwright 集成、代理配置、AI 智能体场景
