# 安装指南

## 适用场景

- 安装 Scrapling 核心库并配置浏览器驱动
- 在 Docker 环境中使用预置镜像
- 为不同 Fetcher 安装对应依赖

---

## 基础安装

> **AI 可自动执行**

```bash
pip install scrapling
```

验证安装：
```bash
python -c "import scrapling; print(scrapling.__version__)"
```

---

## 按需安装浏览器驱动

Scrapling 有三种 Fetcher，各需不同依赖：

### Fetcher（纯 HTTP，无需额外驱动）

```bash
pip install scrapling
# 无需额外安装，开箱即用
```

### StealthyFetcher（隐身模式，需要 Camoufox）

```bash
pip install scrapling
scrapling install camoufox   # 安装修改版 Firefox 驱动
```

或手动安装：
```bash
pip install camoufox[geoip]
python -m camoufox fetch
```

### DynamicFetcher（完整浏览器自动化，需要 Playwright）

```bash
pip install scrapling
scrapling install playwright   # 安装 Playwright 和 Chromium
```

或手动安装：
```bash
pip install playwright
playwright install chromium
```

---

## 一次性安装全部依赖

```bash
pip install scrapling
scrapling install all
```

---

## Docker 安装（推荐生产环境）

使用官方预置镜像（含所有浏览器驱动）：

```bash
# 拉取最新镜像
docker pull d4vinci/scrapling:latest

# 运行容器
docker run -it d4vinci/scrapling:latest python3

# 在容器内直接使用
docker run --rm d4vinci/scrapling:latest python3 -c "
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch('https://example.com', headless=True)
print(page.css('title::text').get())
"
```

---

## 虚拟环境（推荐）

```bash
python -m venv scrapling-env
source scrapling-env/bin/activate   # Windows: scrapling-env\Scripts\activate
pip install scrapling
scrapling install playwright
```

---

## MCP 服务器安装（AI 集成）

Scrapling 内置 MCP 服务器，让 Claude/Cursor 等 AI 直接调用：

### Claude Code

```bash
claude mcp add scrapling --scope user npx -y scrapling-mcp
```

或手动安装后配置：
```json
{
  "mcpServers": {
    "scrapling": {
      "command": "python",
      "args": ["-m", "scrapling.mcp"]
    }
  }
}
```

### 直接启动 MCP 服务器

```bash
scrapling mcp
```

---

## 验证安装

```python
# 验证核心安装
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://httpbin.org/get')
print(page.status)  # 期望：200

# 验证 Playwright（DynamicFetcher）
from scrapling.fetchers import DynamicFetcher
page = DynamicFetcher.fetch('https://example.com', headless=True)
print(page.css('title::text').get())

# 验证 Camoufox（StealthyFetcher）
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch('https://example.com', headless=True)
print(page.css('title::text').get())
```

---

## 完成确认检查清单

- [ ] `pip install scrapling` 执行成功
- [ ] `python -c "import scrapling"` 无报错
- [ ] 按需安装了 Playwright 或 Camoufox（视场景而定）
- [ ] `Fetcher.get('https://httpbin.org/get').status == 200` 验证通过

---

## 下一步

- [快速开始](02-quickstart.md) — Fetcher 选型指南、CSS/XPath 选择器、自适应抓取
