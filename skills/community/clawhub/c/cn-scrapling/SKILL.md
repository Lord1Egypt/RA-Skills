---
name: scrapling
description: 高性能自适应 Python 网页抓取框架，内置反爬虫绕过（Cloudflare Turnstile）、智能元素重定位、完整爬虫框架和 MCP 服务器，适合 AI 辅助数据提取和大规模爬取任务
version: 0.1.0
metadata:
  openclaw_requires: ">=1.0.0"
  emoji: 🕷️
  homepage: https://scrapling.readthedocs.io
---

# Scrapling — 自适应网页抓取框架

Scrapling 是 Google Chrome DevTools 生态之外最强大的 Python 网页抓取框架之一，能够处理从单次 HTTP 请求到大规模并发爬取的所有场景。它的自适应解析引擎在网页改版后自动重新定位元素，内置 Cloudflare Turnstile 绕过能力，Spider 框架支持暂停/恢复，并提供 MCP 服务器让 AI 直接辅助数据提取，从源头减少 Token 消耗。

## 核心使用场景

- **反爬虫网站抓取**：`StealthyFetcher` 内置 Cloudflare Turnstile 绕过，支持 TLS 指纹伪装和浏览器自动化
- **自适应数据采集**：网页改版后，`auto_save=True` 保存元素快照，`adaptive=True` 自动重新定位变化元素
- **大规模并发爬取**：Spider 框架支持多 Session、代理轮换、暂停恢复，像 Scrapy 一样定义爬虫
- **AI 辅助提取**：内置 MCP 服务器，Claude/Cursor 等 AI 工具可直接调用 Scrapling 提取目标内容
- **动态页面处理**：`DynamicFetcher` 基于 Playwright，支持完整浏览器自动化和网络空闲等待

## AI 辅助使用流程

1. **安装依赖** — AI 执行 `pip install scrapling` 并按需安装浏览器驱动
2. **选择 Fetcher** — AI 根据目标网站类型推荐 `Fetcher`/`StealthyFetcher`/`DynamicFetcher`
3. **编写抓取逻辑** — AI 生成 CSS/XPath 选择器代码，配置 `auto_save` 实现自适应
4. **调试与优化** — AI 分析响应结果，调整选择器或切换 Fetcher 策略
5. **扩展为 Spider** — AI 将单页抓取扩展为完整 Spider 类，配置并发和代理
6. **MCP 模式** — 启动 Scrapling MCP Server，让 AI 直接操控浏览器提取数据

## 关键章节导航

- [安装指南](guides/01-installation.md) — pip 安装、浏览器驱动、Docker 镜像
- [快速开始](guides/02-quickstart.md) — Fetcher 选型、CSS/XPath 选择器、自适应抓取
- [高级用法](guides/03-advanced-usage.md) — Spider 框架、代理轮换、MCP 服务器、CLI 工具
- [故障排查](troubleshooting.md) — 反爬虫、浏览器驱动、超时、代理问题

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 安装 Scrapling 并配置浏览器驱动（`scrapling install playwright` / `scrapling install camoufox`）
- ✅ 根据目标网站自动选择最合适的 Fetcher 类
- ✅ 编写 CSS/XPath 选择器提取目标数据
- ✅ 配置 `auto_save=True` 和 `adaptive=True` 实现自适应抓取
- ✅ 构建完整的 Spider 类实现并发爬取，配置暂停/恢复
- ✅ 设置代理轮换和防 DNS 泄露（DoH 模式）
- ✅ 启动和配置 Scrapling MCP 服务器
- ✅ 使用 CLI 工具快速测试 URL 抓取效果

## 核心功能

- ✅ **三种 Fetcher** — `Fetcher`（快速 HTTP）、`StealthyFetcher`（反爬绕过）、`DynamicFetcher`（浏览器自动化）
- ✅ **自适应解析** — 网页改版后自动重定位元素，降低维护成本
- ✅ **Cloudflare 绕过** — 内置 Turnstile/Interstitial 解决方案，免额外服务
- ✅ **Spider 框架** — Scrapy 风格 API，支持并发、多 Session、暂停恢复
- ✅ **流式输出** — `spider.stream()` 实时推送抓取结果，适合大规模任务
- ✅ **MCP 服务器** — AI 工具直接调用 Scrapling 提取数据，减少 Token 消耗
- ✅ **代理轮换** — 内置 `ProxyRotator`，支持循环或自定义策略
- ✅ **会话管理** — `FetcherSession`/`StealthySession`/`DynamicSession` 跨请求保持状态
- ✅ **开发模式** — 首次运行缓存响应，后续离线回放，快速迭代解析逻辑
- ✅ **CLI 工具** — 无需写代码直接从终端抓取页面
- ✅ **IPython Shell** — 交互式调试，内置 curl 转换工具
- ✅ **Docker 镜像** — 预置所有浏览器的生产就绪镜像

## 快速示例

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher

# 普通 HTTP 抓取（最快）
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()

# 隐身模式绕过 Cloudflare
page = StealthyFetcher.fetch('https://protected-site.com', headless=True)
data = page.css('.content::text').get()

# 自适应抓取（网站改版后自动重定位）
page = Fetcher.get('https://example.com/products')
products = page.css('.product', auto_save=True)   # 首次保存元素快照
# 网站改版后：
products = page.css('.product', adaptive=True)    # 自动重新定位
```

```bash
# CLI 快速测试（无需写代码）
scrapling fetch https://quotes.toscrape.com/ --css ".quote .text"

# 启动 MCP 服务器
scrapling mcp
```

## 安装要求

| 依赖 | 版本要求 |
|------|---------|
| Python | >= 3.9 |
| pip | 任意版本 |
| Playwright | 可选（DynamicFetcher 使用） |
| Camoufox | 可选（StealthyFetcher 使用） |
| Docker | 可选（使用官方镜像） |

## 项目链接

- GitHub：https://github.com/D4Vinci/Scrapling
- 文档：https://scrapling.readthedocs.io/en/latest/
- PyPI：https://pypi.org/project/scrapling/
- MCP 文档：https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html
- Discord：https://discord.gg/EMgGbDceNQ
