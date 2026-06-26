# 故障排查

## 安装问题

---

### 问题 1：`camoufox` 安装失败或 `scrapling install camoufox` 报错

**难度：** 低

**症状：** `ERROR: Could not build wheels for camoufox` 或 `ModuleNotFoundError: No module named 'camoufox'`

**排查步骤：**
```bash
pip show camoufox
python --version  # 需要 >= 3.9
```

**解决方案：**
```bash
# 方式一：通过 scrapling 安装
pip install scrapling
scrapling install camoufox

# 方式二：直接安装（含 GeoIP 数据）
pip install "camoufox[geoip]"
python -m camoufox fetch

# 如果遇到编译错误，先升级 pip
pip install --upgrade pip setuptools wheel
pip install "camoufox[geoip]"
```

---

### 问题 2：Playwright 安装后浏览器找不到

**难度：** 低

**症状：** `BrowserNotFoundError: Executable doesn't exist at ...` 或 `Playwright requires browser binaries`

**解决方案：**
```bash
# 必须在安装 playwright 包后，额外下载浏览器
pip install playwright
playwright install chromium   # 只装 Chromium（体积小）
# 或
playwright install            # 安装所有浏览器

# 验证
playwright --version
python -c "from playwright.sync_api import sync_playwright; sync_playwright().start()"
```

---

### 问题 3：Linux 服务器缺少系统依赖

**难度：** 中

**症状：** `error while loading shared libraries: libatk-1.0.so.0` 或类似 `libXXX.so` 缺失错误

**解决方案：**
```bash
# Ubuntu/Debian
playwright install-deps chromium

# 或手动安装
sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
  libgbm1 libpango-1.0-0 libcairo2 libasound2

# 推荐：直接使用 Docker 镜像避免依赖问题
docker pull d4vinci/scrapling:latest
```

---

## 使用问题

---

### 问题 4：Cloudflare 或反爬虫未被绕过

**难度：** 中

**症状：** 返回 403 状态码、Cloudflare 验证页面 HTML、或空白内容

**常见原因：**
- 使用了普通 `Fetcher` 而不是 `StealthyFetcher`（概率 50%）
- `headless=True` 模式下被检测（概率 30%）
- 需要 `solve_cloudflare=True` 参数（概率 20%）

**解决方案：**
```python
from scrapling.fetchers import StealthyFetcher

# 基础反爬绕过
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    headless=True,
    network_idle=True
)
print(page.status)  # 期望 200

# Cloudflare Turnstile 专用参数
page = StealthyFetcher.fetch(
    'https://cloudflare-site.com',
    headless=True,
    solve_cloudflare=True,    # 自动处理 Turnstile
    google_search=False        # 不模拟来自 Google 搜索
)

# 检查是否被拦截
if 'cloudflare' in page.html.lower() or page.status == 403:
    print("仍被拦截，尝试 headless=False（有头模式）")
```

---

### 问题 5：`adaptive=True` 找不到元素（返回空列表）

**难度：** 中

**症状：** `products = page.css('.product', adaptive=True)` 返回 `[]`

**常见原因：**
- 从未使用 `auto_save=True` 保存过该元素的快照（概率 60%）
- 快照数据库路径不一致（概率 25%）
- 网页结构变化太大，相似度算法无法匹配（概率 15%）

**解决方案：**
```python
# 步骤 1：确认先用 auto_save 保存过快照
page = Fetcher.get('https://example.com/products')
products = page.css('.product', auto_save=True)  # 必须先保存
print(f"已保存 {len(products)} 个元素快照")

# 步骤 2：检查快照数据库存在
import os
db_path = os.path.expanduser('~/.scrapling/storage.db')
print(f"数据库存在: {os.path.exists(db_path)}")

# 步骤 3：验证 adaptive 模式
page = Fetcher.get('https://example.com/products')
products = page.css('.product', adaptive=True)
print(f"自适应找到 {len(products)} 个元素")
```

---

### 问题 6：Spider 爬取速度过慢

**难度：** 中

**症状：** 爬虫运行时 CPU 占用低，但进度很慢

**解决方案：**
```python
from scrapling.spiders import Spider

class FastSpider(Spider):
    name = "fast"
    start_urls = ["https://example.com/"]
    
    # 增加并发（根据目标网站承受能力调整）
    concurrent_requests = 20
    
    # 减少延迟（礼貌爬取建议 >= 0.5）
    download_delay = 0.2
    
    # 禁用 robots.txt 检查（如确认不需要）
    robots_txt_obey = False
    
    async def parse(self, response):
        pass
```

也可以改用异步 Fetcher 批量并发：
```python
import asyncio
from scrapling.fetchers import AsyncFetcher

async def main():
    urls = ["https://example.com/page/{}".format(i) for i in range(100)]
    async with AsyncFetcher() as f:
        results = await asyncio.gather(*[f.get(u) for u in urls])
```

---

### 问题 7：CSS 选择器或 XPath 返回空结果

**难度：** 低

**症状：** `.get()` 返回 `None`，`.getall()` 返回 `[]`

**排查步骤：**
```python
page = Fetcher.get('https://example.com')

# 1. 确认页面已加载
print(page.status, len(page.html))

# 2. 检查页面是否需要 JS 渲染
if '<noscript>' in page.html or 'Please enable JavaScript' in page.html:
    print("需要切换到 DynamicFetcher")

# 3. 打印页面结构
print(page.css('body').get()[:500])

# 4. 用交互式 Shell 调试
# scrapling shell https://example.com
```

**解决方案：**
```python
# 如果页面需要 JS 渲染，切换 Fetcher
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.fetch('https://example.com', headless=True, network_idle=True)
data = page.css('.dynamic-content::text').getall()
```

---

## 网络/环境问题

---

### 问题 8：代理连接失败

**难度：** 中

**症状：** `ProxyError: Cannot connect to proxy` 或 `407 Proxy Authentication Required`

**排查步骤：**
```bash
# 先验证代理是否可用
curl -x "http://user:pass@proxy.example.com:8080" https://httpbin.org/ip
```

**解决方案：**
```python
from scrapling.fetchers import Fetcher

# 确认代理格式正确（包含协议头）
proxy = "http://username:password@proxy.example.com:8080"
page = Fetcher.get('https://httpbin.org/ip', proxy=proxy)
print(page.json()['origin'])  # 应显示代理 IP

# SOCKS5 代理
proxy_socks = "socks5://user:pass@proxy.example.com:1080"
page = Fetcher.get('https://httpbin.org/ip', proxy=proxy_socks)
```

---

### 问题 9：并发爬取触发目标网站限流（429）

**难度：** 中

**症状：** 大量请求返回 `429 Too Many Requests` 或被封禁

**解决方案：**
```python
from scrapling.spiders import Spider

class PoliteSipder(Spider):
    name = "polite"
    start_urls = ["https://example.com/"]
    
    # 降低并发和增加延迟
    concurrent_requests = 3
    download_delay = 2.0            # 2 秒间隔
    randomize_download_delay = True  # 随机化延迟（更自然）
    
    # 配合代理轮换
    proxies = ["http://proxy1:8080", "http://proxy2:8080"]

    async def parse(self, response):
        if response.status == 429:
            # 触发重试（Spider 会自动重试）
            return
```

---

## 通用诊断

```python
# 快速诊断页面获取情况
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')
print({
    "status": page.status,
    "html_length": len(page.html),
    "title": page.css('title::text').get(),
    "url": page.url,
})
```

```bash
# CLI 快速诊断
scrapling fetch https://example.com --html | head -50

# 交互式调试
scrapling shell https://example.com
```

**文档：** https://scrapling.readthedocs.io/en/latest/

**GitHub Issues：** https://github.com/D4Vinci/Scrapling/issues

**Discord 社区：** https://discord.gg/EMgGbDceNQ
