# 🔑 媳妇智投全球通用版 v4.0 Global — Data Configuration Guide / 数据接口配置指南

> 📌 **Core Principle / 核心原则: This skill contains NO built-in API keys!**
> You configure the data sources, you unlock the markets.
> 您配置什么接口，就解锁哪些国家的数据。
>
> ⚠️ **Template data is for illustration only.** Real market data requires configured APIs.
> **模板数据仅为演示用途。** 真实市场数据需要配置API后才能获取。

---

## Quick Start / 快速入口

| Your Need / 你的需求 | Go Here / 看这里 |
|:--------|:------|
| 🇨🇳 **A-Share only / 只做A股** | → [Guosen API / 国信证券API](#option-1-guosen-securities-api--国信证券api) |
| 🇺🇸 **US Stocks only / 只做美股** | → [Sina Finance (zero config / 零配置)](#option-3-sina-finance-free-zero-config--新浪财经免费零配置) |
| 🌐 **Global 52 countries / 全球52国通吃** | → [Yahoo Finance / yfinance](#option-2-yahoo-finance-recommended-for-global--全球推荐) |
| 🇨🇳+🌐 **Best coverage / 全能选手** | → [Guosen + yfinance combo](#recommended-setups--数据源搭配方案推荐) |

---

## Option 1: Guosen Securities API / 国信证券API

**Covers / 覆盖范围:** 🇨🇳A-Share all stocks + 🇺🇸US all stocks + 🇭🇰HK all stocks

### How to Get API Key / 获取API Key

```
Step 1: Visit / 访问 https://www.guosen.com.cn/gs/xxskills/index.html
Step 2: Register & Login / 注册并登录
Step 3: Click "Login" button at top / 点击顶部「登录」
Step 4: After login, click account name → copy API Key / 点击账号→弹窗中复制密钥
```

### Configure Environment Variable / 配置环境变量

```bash
# macOS / Linux (add to ~/.bashrc or ~/.zshrc)
export GS_API_KEY="your_guosen_api_key_here"

# Or for current terminal session / 或者临时生效
export GS_API_KEY="your_guosen_api_key_here"

# Windows PowerShell
$env:GS_API_KEY = "your_guosen_api_key_here"
```

### Verify / 验证

```bash
# A-Share / A股
GS_API_KEY="your_key" python3 scripts/generate_plan.py single_hq --code 600519 --set_code 1

# US Stocks / 美股 (setCode=74)
GS_API_KEY="your_key" python3 scripts/generate_plan.py single_hq --code AAPL --set_code 74 --target 3

# HK Stocks / 港股 (setCode=-1)
GS_API_KEY="your_key" python3 scripts/generate_plan.py single_hq --code 00700 --set_code -1 --target 3
```

---

## Option 2: Yahoo Finance (Recommended for Global / 全球推荐)

**Covers / 覆盖范围:** 🌐 **All 52 countries / 全部52国**

### Method A: yfinance (Free, Recommended / 免费推荐)

yfinance is an open-source Python library for Yahoo Finance. **No API key needed, completely free.**

**Install / 安装:**
```bash
pip3 install yfinance --upgrade
```

**Verify / 验证:**
```bash
python3 << 'EOF'
import yfinance as yf

# Test stocks from different countries / 测试不同国家的股票
tests = [
    ("SHEL.L", "🇬🇧 UK Shell / 英国壳牌"),
    ("7203.T", "🇯🇵 Japan Toyota / 日本丰田"),
    ("SAP.DE", "🇩🇪 Germany SAP"),
    ("MC.PA", "🇫🇷 France LVMH"),
    ("005930.KS", "🇰🇷 S.Korea Samsung / 韩国三星"),
    ("NESN.SW", "🇨🇭 Switzerland Nestle / 瑞士雀巢"),
    ("BHP.AX", "🇦🇺 Australia BHP / 澳洲必和必拓"),
    ("RELIANCE.NS", "🇮🇳 India Reliance / 印度信实"),
    ("SHOP.TO", "🇨🇦 Canada Shopify"),
    ("D05.SI", "🇸🇬 Singapore DBS / 新加坡星展"),
    ("2222.SR", "🇸🇦 Saudi Aramco / 沙特阿美"),
    ("PETR4.SA", "🇧🇷 Brazil Petrobras / 巴西石油"),
    ("AGL.JO", "🇿🇦 S.Africa AngloGold / 南非"),
    ("AD.AS", "🇳🇱 Netherlands / 荷兰"),
]

for code, name in tests:
    stock = yf.Ticker(code)
    info = stock.info
    price = info.get('currentPrice') or info.get('regularMarketPrice')
    if price:
        print(f"✅ {name:<30} {code:<12} ${price:.2f}")
    else:
        print(f"❌ {name:<30} {code:<12} No data")
EOF
```

**If you get `YFRateLimitError`:**
Cloud server IPs are sometimes rate-limited by Yahoo. **Solution:** Run on your home/office computer, or use a proxy.

```bash
# Use a proxy if available / 如果有代理
export HTTP_PROXY="http://your_proxy:port"
export HTTPS_PROXY="http://your_proxy:port"
```

### Method B: Alpha Vantage (Backup / 备用)

Free tier: 5 requests/minute

1. Visit https://www.alphavantage.co/support/#api-key
2. Register for free API key
3. Configure:
```bash
export ALPHA_VANTAGE_KEY="your_key"
```

---

## Option 3: Sina Finance (Free, Zero Config / 新浪财经免费零配置)

**Covers / 覆盖范围:** 🇨🇳A-Share real-time + 🇺🇸US Stocks real-time

**No configuration needed! Works out of the box.**
**无需任何配置，开箱即用！**

**Verify / 验证:**
```bash
python3 << 'EOF'
import urllib.request

# US Stocks / 美股
url = 'https://hq.sinajs.cn/list=gb_aapl,gb_nvda,gb_tsla'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn/stock/usstock/',
})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = resp.read().decode('gbk')
    for line in data.strip().split('\n'):
        parts = line.split('"')[1].split(',')
        print(f"{parts[0]}: ${float(parts[1]):.2f}")
EOF
```

**Supported US stocks（部分支持的美股）:**
AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, JPM, V, BA, XOM, WMT, DIS, GE, CVX, PG, KO, HD, INTC, AMD, SHEL, TM — **thousands of US stocks / 数千只**

---

## Option 4: Tushare (A-Share Financial Data / A股财务数据补充)

**Covers / 覆盖范围:** 🇨🇳A-Share financial data supplement

**How to get token / 获取流程:**
```
1. Visit / 访问 https://tushare.pro/
2. Register & Login / 注册登录
3. Profile → API Token / 个人主页→接口TOKEN
4. Copy your token / 复制Token
```

**Configure / 配置:**
```bash
export TUSHARE_TOKEN="your_tushare_token"
```

---

## Recommended Setups / 数据源搭配方案推荐

| Your Need / 需求 | Recommendation / 推荐方案 | Effort / 工作量 | Quality / 数据质量 |
|:--------|:--------|:--------:|:-------:|
| 🇨🇳 **A-Share only / 只做A股** | Guosen API + Tushare | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 🇺🇸 **US Stocks only / 只做美股** | Sina Finance (zero config) | ⭐ | ⭐⭐⭐ |
| 🇺🇸+🇨🇳 **US + China** | Guosen API + Sina Finance | ⭐⭐ | ⭐⭐⭐⭐ |
| 🌐 **Global 52 countries / 全球52国** | **yfinance** (free, one-install) | ⭐ | ⭐⭐⭐⭐ |
| 🇨🇳+🌐 **Ultimate combo / 全能选手** | Guosen API + yfinance + Tushare | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recommended / 推荐: yfinance + Guosen API** → A-shares via Guosen (stable) + Global via yfinance (52 countries) → Best of both worlds!

---

## 🔄 How to Use Auto Switch / 如何使用自动切换

Just type a stock symbol — the system auto-detects the country. / 直接输入代码，自动识别国家。

| You Type / 你输入 | Auto-Detected / 自动识别为 |
|:-----------------|:-------------------------|
| `600519` / `000001` / `300750` | 🇨🇳 A-Share / A股 |
| `AAPL` / `NVDA` / `TSLA` | 🇺🇸 US Stock / 美股 |
| `0700` / `00700` / `09988` | 🇭🇰 HK Stock / 港股 |
| `SHEL.L` / `HSBA.L` / `BP.L` | 🇬🇧 UK / 英国 |
| `7203.T` / `6758.T` / `9984.T` | 🇯🇵 Japan / 日本 |
| `SAP.DE` / `BAYN.DE` / `VOW3.DE` | 🇩🇪 Germany / 德国 |
| `005930.KS` / `000660.KS` | 🇰🇷 S.Korea / 韩国 |
| `RELIANCE.NS` / `TCS.NS` | 🇮🇳 India / 印度 |
| `PETR4.SA` / `VALE3.SA` | 🇧🇷 Brazil / 巴西 |
| `CBA.AX` / `BHP.AX` | 🇦🇺 Australia / 澳洲 |

**Don't want auto? Just say "Switch to UK" or "切到英国".**
不想自动识别？直接说一句"切到英国"就行。

## Global 52-Country Code Reference / 全球52国代码速查表

```
Input / 输入                          → Market / 识别为
───────────────────────────────────────────────────
600519 / 300750 / 000001               → 🇨🇳 A-Share / A股
0700 / 00700 / 09988                   → 🇭🇰 HK / 港股
AAPL / NVDA / TSLA                     → 🇺🇸 US / 美股

SHEL.L                                 → 🇬🇧 UK / 英国  London
HSBA.L                                 → 🇬🇧 UK HSBC / 汇丰
BP.L                                   → 🇬🇧 UK BP / 英国石油

7203.T                                 → 🇯🇵 Japan Toyota / 丰田
6758.T                                 → 🇯🇵 Japan Sony / 索尼
9984.T                                 → 🇯🇵 Japan SoftBank / 软银

SAP.DE                                 → 🇩🇪 Germany / 德国
BAYN.DE                                → 🇩🇪 Germany Bayer / 拜耳
MC.PA                                  → 🇫🇷 France LVMH / 路易威登
OR.PA                                  → 🇫🇷 France L'Oreal / 欧莱雅
NESN.SW                                → 🇨🇭 Switzerland Nestle / 雀巢
UBSG.SW                                → 🇨🇭 Switzerland UBS / 瑞银

005930.KS                              → 🇰🇷 S.Korea Samsung / 三星
000660.KS                              → 🇰🇷 S.Korea SK Hynix / 海力士
CBA.AX                                 → 🇦🇺 Australia CBA / 联邦银行
BHP.AX                                 → 🇦🇺 Australia BHP / 必和必拓
SHOP.TO                                → 🇨🇦 Canada Shopify
RY.TO                                  → 🇨🇦 Canada RBC / 皇家银行

RELIANCE.NS                            → 🇮🇳 India Reliance / 信实
TCS.NS                                 → 🇮🇳 India TCS / 塔塔咨询
D05.SI                                 → 🇸🇬 Singapore DBS / 星展
AD.AS                                  → 🇳🇱 Netherlands / 荷兰皇家壳牌
2222.SR                                → 🇸🇦 Saudi Aramco / 沙特阿美
PETR4.SA                               → 🇧🇷 Brazil Petrobras / 巴西石油
AGL.JO                                 → 🇿🇦 S.Africa AngloGold / 南非
```

---

## FAQ / 常见问题

**Q: yfinance returns no data / yfinance返回不了数据？**
A: Server IP may be rate-limited. Try running on your home computer. / 服务器IP被限流，试试在家里的电脑运行。

**Q: I only trade A-shares. Do I need yfinance? / 我只做A股，需要yfinance吗？**
A: No. Guosen API is best for A-shares. / 不需要。国信API对A股支持最好。

**Q: I configured Guosen API. Can I also check US stocks? / 配了国信API能查美股吗？**
A: Yes! setCode=74 is the US channel with 30-day K-line data. / 可以。setCode=74就是美股通道，有30天完整K线。

---

**媳妇智投全球通用版 v4.0 Global Edition — Configure what you need, trade where you want 🦊**
**您配置什么，小媳妇就能查什么**
