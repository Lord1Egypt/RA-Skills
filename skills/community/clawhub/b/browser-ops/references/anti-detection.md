# 反爬策略

## 反爬类型与方案

| 反爬类型 | 方案 | 状态 |
|---------|------|------|
| 普通网站 | opencli web read / agent-browser | ✅ |
| 需要登录 | CDP + Cookie 持久化 | ✅ 已验证 |
| 简单验证码 | 手动点一次，后续复用 Cookie | ✅ |
| Cloudflare 盾 | Zendriver / Camoufox | ✅ 已验证 |
| 强指纹检测 | Camoufox（Firefox 内核） | ✅ 已验证 |
| IP 封禁 | 代理池 | ✅ |

## Zendriver（首选，~90% bypass）

Nodriver 同作者的继任项目（async-first 重写），Chrome/Chromium 内核，自动规避常见反爬检测。相比 Nodriver 新增内置 session/cookie 持久化。

```python
import asyncio
import zendriver as zd

async def scrape(url: str):
    browser = await zd.start()
    page = await browser.get(url)
    await page.sleep(3)  # 等待 Cloudflare 验证通过
    content = await page.get_content()
    browser.stop()
    return content

content = asyncio.run(scrape("https://target-site.com"))
```

安装: `pip install zendriver`（需要 Python 3.10+）

> **Note**: Nodriver 已被 Zendriver 取代（同作者 ultrafunkamsterdam）。如已安装 nodriver 可继续使用，但新项目应使用 zendriver。

## Camoufox（备选，~80% bypass）

修改版 Firefox，更难被指纹识别。

```python
from camoufox.sync_api import Camoufox

with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto("https://target-site.com")
    page.wait_for_timeout(3000)
    content = page.content()
```

安装: `pip install camoufox && python3 -m camoufox fetch`

## 云端 fallback

当本地反爬不够时，使用云浏览器：

1. **Zyte**（首选）— 智能代理 + 浏览器渲染
2. **Browserless**（次选）— Docker 化浏览器
3. **Hyperbrowser**（第三）

## 代理配置

```bash
# 按环境配置代理，示例：
export HTTP_PROXY="http://your-proxy-host:port"
export HTTPS_PROXY="http://your-proxy-host:port"
export SOCKS_PROXY="socks5://your-proxy-host:port"

# agent-browser 使用代理
agent-browser --proxy $HTTP_PROXY open https://target-site.com

# Zendriver 使用代理
browser = await zd.start(browser_args=[f"--proxy-server={proxy_url}"])
```

## 住宅代理（Residential Proxy）

高级反爬场景（IP 封禁、地域限制）需要住宅代理。住宅代理使用真实家庭 IP，比数据中心代理更难被检测。

### 推荐供应商

| 供应商 | 价格 | IP 池 | 适用场景 |
|--------|------|-------|---------|
| **Smartproxy/Decodo** | $3-4.5/GB | 55M+ IPs | 性价比最佳，覆盖大多数场景 |
| **Bright Data** | $4-5/GB | 72M+ IPs | 最难目标（银行/政府/大厂反爬） |
| **IPRoyal** | $3.5-5.5/GB | — | 预算有限的备选 |

### 各工具配置住宅代理

**凭证通过环境变量传递**（不要在命令行参数中暴露明文密码）：

```bash
export PROXY_URL="socks5://user:pass@gate.smartproxy.com:7777"
```

```python
import os
proxy_url = os.environ["PROXY_URL"]

# Camoufox + 住宅代理
with Camoufox(proxy={"server": proxy_url}) as browser:
    page = browser.new_page()
    page.goto("https://hard-target.com")

# Zendriver + 住宅代理
browser = await zd.start(browser_args=[f"--proxy-server={proxy_url}"])
```

```bash
# agent-browser + 住宅代理
agent-browser --proxy "$PROXY_URL" open https://hard-target.com
```

### "畅通无阻"组合

最高成功率组合：**Camoufox + 住宅代理**（Firefox 指纹伪装 + 真实家庭 IP）。

适用：被常规反爬拦截且 IP 也被封禁的高难度目标。

### Cloudflare AI Labyrinth (2026)

Cloudflare 于 2026 年推出 AI Labyrinth：不再直接封锁爬虫，而是返回 AI 生成的假页面引诱爬虫进入"迷宫"。症状：内容看似正常但数据完全虚假。应对：对抓取结果做内容校验（对比已知真实数据），检测到假页面时切换住宅代理 + 不同指纹重试。

> See also: `setup.md`（安装）, `routing.md`（路由升级条件）
