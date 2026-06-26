---
name: china-stock-data
description: 中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWencai问财搜索、JQData聚宽量化、Tushare Pro公告、RiceQuant米筐。8大来源自动降级。
version: 2.0.0
metadata:
  hermes:
    tags: [stock, finance, a-share, china-stock, tdx, tencent, tonghuashun, akshare, wencai, monitor, news, cron]
    related_skills: [tonghuashun, stock-announcement-analysis, us-stock-data]
---

# China Stock Data - 中国A股综合数据源

## Overview

本技能集成 **8大数据源 + 3大工具**，覆盖 A 股行情、K线、研报、公告、资金流向、板块排行、热点题材、语义搜索、量化指标、价格预警、每日简报等全场景。数据源自动降级，无需担心单点故障。

| # | 数据源/工具 | 能力 | 状态 |
|---|------------|------|------|
| 1 | **通达信(TDX)** | 实时行情、5档盘口、K线(日/周/月/分钟)、逐笔成交 | ✅ 无需Key |
| 2 | **腾讯财经** | PE、PB、市值、换手率、财务估值数据 | ✅ 公开API |
| 3 | **同花顺(iFinD)** | 专业行情、股息率、热点题材、强势股归因 | ✅ 需配置token |
| 4 | **AKShare** | 券商研报、公司公告、资金流向、补充数据 | ✅ 部分受限 |
| 5 | **iWencai(问财)** | 自然语言选股、跨主题语义搜索 | ⚠️需API Key |
| 6 | **JQData(聚宽)** | 量化指标、财报因子、宏观数据 | ✅ 需账号 |
| 7 | **Tushare Pro** | 公告、日线、北向、两融、财报 | ✅ 需token |
| 8 | **RiceQuant(米筐)** | 量化回测数据 | ✅ 需账号 |
| 9 | **巨潮资讯网(CNINFO)** 🆕 | 公告全文搜索，覆盖深沪两市全部A股 | ✅ 公开API，无需Key |
| 🔔 | **Stock Monitor** | 价格预警、自选异动检查、自动盯盘 | ✅ 内置 |
| 📰 | **News Aggregator** | 每日金融简报、指数行情、头条汇总 | ✅ 内置 |

**本文就是根据这些微信公众号文章搭建的：**
- [用 Claude Code 搭建大A稳定数据源](https://mp.weixin.qq.com/s/wWIJOYwfmzQ5EEIZQbby0Q)
- [A股数据平台及工具大全](https://mp.weixin.qq.com/s/SV2TGAppLlmhvQQYLWDRIw)
- [金融AI工具10选](https://mp.weixin.qq.com/s/M5wRDr1sIoYXRzBDIl6sWA)
选型逻辑：通达信+腾讯财经（行情）→ 东财+AKShare（研报）→ 同花顺（热点）→ iWencai（搜索）→ 聚宽/米筐（量化）→ Monitor+News（监控+简报）

## When to Use

自然语言输入即可查询：

```
# 实时行情（自动选择最佳数据源）
查一下 600519 的行情
贵州茅台现在多少钱
批量看 600519,300750,000001

# K线数据
看下 300750 最近30天K线
宁德时代周K线

# 研报与公告
贵州茅台最近研报
300750 最新公告

# 资金流向
茅台资金流向

# 板块排行
今天什么板块涨得好
行业板块排行

# 热点题材
今天热点题材
同花顺热点

# 问财搜索（需配置Token）
搜索：人形机器人 丝杠
问财：华为概念 业绩预增
```

**不要用于：**
- 下单/交易操作（本技能仅提供数据查询）

## How It Works

所有查询通过 `scripts/china_stock.py` 统一执行。

```bash
SCRIPT=scripts/china_stock.py
PY=python3
```

### 命令速查

```bash
# === 智能行情（自动降级）===
$PY $SCRIPT quote 600519            # TDX → 腾讯 → iFinD自动降级（含PE/市值/换手率）
$PY $SCRIPT tencent-quote 000001    # 腾讯财经行情（平安银行）

# === 通达信（实时+盘口）===
$PY $SCRIPT tdx-quote 600519        # 实时行情+5档买卖盘口
$PY $SCRIPT tdx-kline 600519 daily  # K线 (daily/weekly/monthly/60min/30min/15min/5min)
$PY $SCRIPT tdx-kline 300750 weekly # 周K
$PY $SCRIPT tdx-kline 600519 60min  # 60分钟K线

# === 腾讯财经（财务指标）===
$PY $SCRIPT tencent-quote 000001    # PE/PB/市值/换手率
$PY $SCRIPT tencent-batch 600519,300750,000001  # 批量查询

# === 同花顺iFinD（需token）===
$PY $SCRIPT ifind-quote 600519      # 专业行情（含PE/换手率/股息率/振幅）

# === AKShare（研报/资金）===
$PY $SCRIPT report 600519 10        # 最近10份研报
$PY $SCRIPT moneyflow 600519 5      # 最近5天资金流向

# === 公告查询（三级降级：巨潮CNINFO → Tushare Pro → AKShare）===
$PY $SCRIPT announce 600519 20      # 最近20条公告（自动选最佳源）
$PY $SCRIPT moneyflow 600519 5      # 最近5天资金流向

# === 巨潮资讯网(CNINFO) 公告搜索 — 2026年新增首选公告源 ===
$PY $SCRIPT announce 600519           # 自动降级: CNINFO → Tushare → AKShare
$PY $SCRIPT tushare-ann 600519        # Tushare Pro公告（tushare.xyz自定义地址）

# === 板块排行 & 热点 ===
$PY $SCRIPT sector                  # 行业板块排行  TOP20
$PY $SCRIPT themes                  # 热点题材（行业+概念）

# === 问财语义搜索（需配置 WENCAI_TOKEN）===
$PY $SCRIPT search 人形机器人 丝杠   # 自然语言选股

# === Tushare Pro（公告数据当前可用）===
$PY $SCRIPT tushare-ann 600519 20  # 最新20条公告

# === JQData聚宽（需 export JQ_USER/JQ_PASS）===
$PY $SCRIPT jq-financial 600519    # 财报指标数据
$PY $SCRIPT jq-macro               # 宏观数据（GDP/CPI）

# === Stock Monitor 股票监控 ===
MON=~/.hermes/skills/financial/china-stock-data/scripts/stock_monitor.py
$PY $MON check 600519              # 检查贵州茅台当前价格
$PY $MON check 600519 1300 below   # 检查是否跌破1300
$PY $MON watchlist                 # 自选股异动扫描
$PY $MON watchlist 600519,300750,000001  # 指定列表异动

# === News Aggregator 新闻简报 ===
NEWS=~/.hermes/skills/financial/china-stock-data/scripts/news_aggregator.py
$PY $NEWS daily                    # 当日金融简报（指数+头条）
$PY $NEWS indices                  # 主要指数行情
$PY $NEWS headlines                # 同花顺快讯

# === 系统状态 ===
$PY $SCRIPT status                  # 全部数据源状态
```

### 数据源降级策略

```
行情查询自动按顺序降级：
  [1] 通达信(TDX) ── 5档盘口 + 实时行情
  [2] 腾讯财经    ── 补充PE/市值/换手率（与TDX并行）
  [3] 同花顺iFinD ── 专业级行情（需配置token）

板块排行/热点：
  [1] 同花顺官网  ── 实时行业/概念涨幅排行
  [2] EastMoney   ── 被限流时自动切换同花顺
```

### 股票代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 上海A股 | 6xxxxx | 600519 |
| 深圳主板 | 00xxxx | 000001 |
| 深圳创业板 | 30xxxx | 300750 |
| 科创板 | 688xxx | 688xxx |

脚本自动识别代码前缀（6→沪，0/3→深），无需加 sh/sz 前缀。

## Setup

```bash
# 安装核心依赖
pip install -r requirements.txt

# 或手动安装
pip install pytdx akshare beautifulsoup4 requests lxml pandas openpyxl

# 可选：数据源增强（按需安装）
pip install jqdatasdk    # JQData聚宽量化数据（需账号）
pip install rqdatac      # RiceQuant米筐量化数据（需账号）
pip install tushare      # Tushare Pro综合数据（需token）
pip install wencai       # 同花顺问财语义搜索（需API Key）

# 配置同花顺iFinD token（提升专业行情质量）
# 编辑 ifind_config.json 并放在脚本同目录：
# {"access_token": "your_token", "refresh_token": "your_token"}

# 可选环境变量
export WENCAI_TOKEN=your_token   # 问财搜索
export JQ_USER=your_phone       # JQData账号
export JQ_PASS=your_password    # JQData密码
export RQ_USER=your_username    # RiceQuant账号
export RQ_PASS=your_password    # RiceQuant密码
```

## Data Source Details

### 1️⃣ 通达信(TDX) — 实时交易数据之王
- **协议**: pytdx (开源TCP协议实现)
- **特点**: 无需API Key，直连通达信行情服务器
- **数据**: 实时价格、5档买卖盘口、K线(日/周/月/分钟)、逐笔成交
- **延迟**: 约3-5秒（与通达信客户端同步）
- **限速保护**:
  - 🛡️ 每次TDX调用间隔 ≥0.5秒（随机加0-0.2秒jitter）
  - 🔄 4台服务器轮询（成都电信、北京联通、上海电信、杭州电信）
  - 📦 批量查询优化：指数日报用1次连接查6个指数，而非6次独立连接
- **状态**: ✅ 可用

### 2️⃣ 腾讯财经 — 财务指标补充
- **接口**: `https://qt.gtimg.cn/q={code}`
- **特点**: 公开HTTP API，调用简单
- **数据**: PE(市盈率)、PB(市净率)、市值(总/流通)、换手率
- **状态**: ✅ 可用

### 3️⃣ 同花顺(iFinD) — 专业行情
- **接口**: `https://quantapi.51ifind.com/api/v1/`
- **特点**: 专业级金融数据，含股息率、振幅、PE_TTM
- **数据**: 实时行情、K线、公告(含PDF)、板块排行、热点题材
- **配置**: 需 `ifind_config.json`（access_token + refresh_token）
- **状态**: ✅ 需配置token

### 4️⃣ AKShare — 研报/公告
- **接口**: 开源Python库
- **特点**: 多源聚合（东方财富/新浪等），免费
- **数据**: 券商研报、公司公告、资金流向、补充财务数据
- **注意**: EastMoney接口可能被限流，建议降频调用
- **状态**: ✅ 可用（部分源可能限流）

### 5️⃣ iWencai(问财) — 语义搜索
- **接口**: 同花顺问财API（需SkillHub API Key）
- **特点**: 自然语言选股，独一档的语义搜索能力
- **数据**: 跨主题筛选、复杂选股条件
- **配置**: 设置环境变量 `WENCAI_TOKEN`
- **获取Key**: 访问 [SkillHub](https://skillhub.com) 或联系文章作者
- **状态**: ⚠️ 待配置（已实现接口封装）

### 6️⃣ JQData(聚宽) — 量化因子与宏观数据
- **接口**: `jqdatasdk` (Python SDK)
- **特点**: 免费注册可用，提供量化指标、财报因子、宏观数据
- **数据**: 基本面指标、GDP/CPI等宏观、因子数据
- **配置**: `export JQ_USER=手机号 JQ_PASS=密码`
- **注册**: [JoinQuant聚宽官网](https://www.joinquant.com/) 免费注册
- **状态**: ✅ 需配置账号

### 7️⃣ Tushare Pro — 综合数据平台
- **接口**: `tushare` Python SDK (HTTP API)
- **特点**: 免费注册得基础积分，签到/分享可获取更多积分
- **数据**: 公告、日线、北向、两融、财报（⚠️高级数据需积分）
- **配置**: 在脚本中设置 `token`，国内用户需配置自定义URL：`client.DataApi._DataApi__http_url = "http://tushare.xyz"`
- **注册**: [Tushare Pro官网](https://tushare.pro/) 注册获取token
- **状态**: ✅ 需配置账号和token

### 8️⃣ RiceQuant(米筐) — 量化回测数据
- **接口**: `rqdatac` (Python SDK)
- **特点**: 免费注册可用，提供回测数据和研究环境
- **配置**: `export RQ_USER=用户名 RQ_PASS=密码`
- **状态**: ✅ 已安装，需认证

## References

| 文件 | 内容 |
|------|------|
| `scripts/china_stock.py` | 主脚本，8大数据源集成（行情/K线/研报/公告/资金/板块/搜索/量化） |
| `scripts/stock_monitor.py` | 股票监控/预警（价格检查、自选异动、可配cronjob定时盯盘） |
| `scripts/news_aggregator.py` | 金融新闻聚合（每日简报、指数行情、头条快讯） |
| `requirements.txt` | Python依赖列表 |
| `references/tdx-protocol-notes.md` | TDX通达信协议细节 + 限速策略 |
| `references/eastmoney-limitations.md` | EastMoney限流备忘 / 替代方案 |
| `references/tdx-rate-limiting.md` | TDX限速策略文档（全局间隔/服务器轮询/批量查询） |
| `references/tonghuashun-headlines-api.md` | 同花顺快讯API响应结构说明 |
| `references/cninfo-api.md` | 巨潮CNINFO公告API接口文档 |
| `references/cninfo-pdf-extraction.md` | CNINFO PDF下载方法（浏览器工具） |

## Common Pitfalls

1. **TDX服务器可能变化** — 脚本内置了4台服务器（成都、北京、上海、杭州），自动轮询+最多尝试4次。每次调用间隔≥0.5秒，防被封IP
2. **腾讯财经字段索引** — 返回的 `~` 分隔字符串，按固定顺序解析（0:市场 1:名称 2:代码 3:现价 4:昨收 ...）
3. **EastMoney被限流** — 服务器IP可能被东方财富临时封禁，板块排行已自动切换到同花顺页面抓取
4. **iFinD Token过期** — iFinD access_token 7天有效，脚本自动用 refresh_token 刷新
5. **iWencai需API Key** — 问财搜索目前被IP级别封禁（403），需通过 SkillHub 获取 API Key 配置后使用
6. **行业板块 vs 概念板块** — 同花顺行业板块(thshy)可直接抓取HTML表格数据；概念板块(gn)为历史事件列表，不是当前涨幅排行
7. **港股/美股支持** — 当前脚本主要面向A股，港股/美股需通过其他工具查询
8. **pandas降级风险** — 安装 jqdatasdk 或 rqdatac 时会自动降级 pandas 至 2.3.x，可能影响 akShare 等依赖新版 pandas 的库。降级后需执行 `pip install --upgrade pandas` 恢复
9. **同花顺快讯 API 响应结构变化 (2026-05)** — `data` 现在是对象 `{"list":[...], "filter":..., "total": N}` 而非数组。字段 `share_url` → `shareUrl`
10. **公告查询优先走巨潮 CNINFO** — 三级降级：CNINFO(全文搜索) → Tushare Pro → AKShare。CNINFO 不需要 Key/Token
11. **CNINFO PDF下载需用浏览器工具** — 巨潮公告详情页的PDF地址是动态生成的，需用浏览器打开详情页获取真实链接

## Verification Checklist

- [x] `quote 600519` — TDX行情含PE/市值/换手率
- [x] `tdx-quote 600519` — 实时价格+5档盘口
- [x] `tdx-kline 300750 daily` — 30条日K线
- [x] `tencent-quote 000001` — 平安银行PE/市值
- [x] `sector` — 行业板块排行TOP20
- [x] `themes` — 行业+概念热点
- [x] `status` — 全部数据源状态
- [ ] `search 人形机器人 丝杠` — 需配置WENCAI_TOKEN
- [ ] `report 600519` — AKShare研报（可能限流）
