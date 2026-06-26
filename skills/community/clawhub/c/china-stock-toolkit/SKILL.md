---
name: china-stock-toolkit
description: 全球市场实时仪表盘 - A股/港股/美股/日韩指数、贵金属、外汇、自选股管理、个股详情分析、交易税费计算。内置多源聚合引擎（新浪/腾讯/东方财富），自动交叉验证数据可靠性。支持用户自定义数据接口扩展。Global market real-time dashboard with multi-source data aggregation, cross-validation, and HTML dashboard. GitHub: https://github.com/darbling/clawhub-skills 当用户询问A股行情、港股、美股、黄金、白银、汇率、自选股、个股分析、新闻、利好利空、交易税费、情绪分析时触发。
---

# 🌍 全球市场实时仪表盘 — china-stock-toolkit

**Author: Lin Hui** | [GitHub](https://github.com/darbling/clawhub-skills) | MIT License | v3.0.0

一个技能看遍全球市场。内置多源聚合引擎，自动交叉验证数据可靠性。

## ⚠️ 免责声明（重要）

**本工具仅供学习和技术研究使用，不构成任何投资建议、交易信号或财务指导。**

1. **非投资建议**：本工具展示的所有数据（包括但不限于指数行情、涨跌停统计、北向资金流向、外汇汇率）仅供参考，不构成买入、卖出或持有任何证券的建议。
2. **数据延迟**：默认免费数据源可能存在延迟（通常15-30分钟），不应作为实时交易决策依据。
3. **数据准确性**：尽管采用多源交叉验证机制，但仍无法保证数据的绝对准确性和完整性。
4. **风险自担**：用户基于本工具数据做出的任何投资决策，其风险和后果由用户自行承担。
5. **非专业服务**：本工具并非持牌证券咨询服务，不能替代专业金融机构的投资建议。
6. **税费计算**：交易税费计算结果仅供参考，实际费用以券商结算为准，各券商费率可能不同。

**使用本工具即表示您已阅读、理解并同意上述免责声明。如果您不同意，请立即停止使用。**

---

## 🌍 支持的市场与数据源

### ✅ 免费数据源（开箱即用）

| 市场 | 指数/品种 | 数据源 | 更新频率 | 状态 |
|------|----------|--------|----------|------|
| A股指数 | 上证/深证/创业板/科创50/北证50 | 腾讯/新浪/东方财富 | 实时 | ✅ 可用 |
| 港股 | 恒生指数 | 腾讯 | 实时 | ✅ 可用 |
| 贵金属 | 黄金/白银 | 腾讯 | 实时 | ✅ 可用 |
| A股个股 | 所有A股 | 腾讯/新浪/东方财富 | 实时 | ✅ 可用 |

### 🔧 扩展数据源（需用户配置）

| 市场 | 指数/品种 | 推荐数据源 | 配置方式 |
|------|----------|-----------|----------|
| 美股指数 | 道琼斯/纳斯达克/标普500 | Yahoo Finance | `export YAHOO_API_KEY=xxx` |
| 日韩指数 | 日经225/韩国KOSPI | Yahoo Finance | 同上 |
| 外汇 | 美元/人民币等 | Alpha Vantage | `export ALPHA_VANTAGE_KEY=xxx` |
| 加密货币 | BTC/ETH | CoinGecko API | 免费无需Key |
| 新浪国际 | 美股/日韩/外汇 | HTTP代理 | `export HTTP_PROXY=http://127.0.0.1:7890` |

---

## 🎯 核心功能

### 1. 📊 全球指数大盘

**A股（开箱即用）**
- 上证指数、深证成指、创业板指、科创50、北证50
- 实时价格、涨跌幅、成交额
- 多源聚合 + 交叉验证

**港股（开箱即用）**
- 恒生指数

**美股/日韩（需配置）**
- 道琼斯、纳斯达克、标普500
- 日经225、韩国KOSPI

### 2. 💰 大宗商品

**贵金属（开箱即用）**
- 黄金（XAU）、白银（XAG）
- 实时价格、涨跌幅

**原油/其他（需配置）**
- WTI、布伦特原油
- 铜、铝等商品

### 3. ⭐ 自选股管理

- 添加/删除自选股
- 实时行情刷新
- 涨跌幅排序
- 点击查看个股详情

### 4. 📰 新闻聚合 + 情感分析 ⭐ **NEW**

智能抓取个股/板块相关新闻，自动标注**利好 📈 / 利空 📉 / 中性 ➡️**：

- **个股新闻**：抓取东方财富、新浪财经的公司新闻和公告
- **板块新闻**：新能源、芯片、人工智能等板块动态  
- **政策追踪**：财联社快讯 + 监管政策实时更新
- **情感分析**：基于200+利好词、150+利空词的关键词库，自动判断新闻情绪
- **情绪汇总**：统计利好/利空比例，给出整体市场情绪（看涨/看跌/观望）

**情感分析原理**：
```
新闻标题: "公司业绩大增50%，超预期"
  ↓ 关键词匹配
  利好词: [增长, 大增, 超预期] → 3个
  利空词: [] → 0个
  ↓ 计算得分
  得分 = (3-0)/(3+0) = 1.0
  ↓ 判断
  情感: 利好 📈
```

**使用场景**：
- 选中一只股票 → 查看最新5条新闻 + 情感标注
- 关心新能源板块 → 查看板块整体情绪（看涨/看跌）
- 关注政策动向 → 实时追踪监管政策新闻

### 5. 📈 个股详情分析

点击任意股票查看多维度分析：
- **基础行情**：价格、涨跌幅、成交量、成交额
- **技术指标**：MA5/MA10/MA20、RSI、MACD
- **资金流向**：主力净流入、散户流向
- **涨跌停分析**：封单量、炸板次数（如适用）
- **税费计算**：自动代入当前价，计算卖出费用
- **持仓盈亏**：记录买入价，实时计算浮动盈亏
- **相关新闻**：自动关联最新5条新闻 + 情感标注 📰

### 6. 🧮 交易税费计算器

- 买入/卖出费用精确计算
- 印花税（卖出千分之0.5）
- 佣金（默认万分之三，可自定义）
- 过户费（十万分之一）
- 盈亏计算 + 收益率

---

## 🔧 多源数据架构

```
用户查询：上证指数
  ├─ 腾讯财经 API → 4078.64
  ├─ 新浪财经 API → 4078.60
  ├─ 东方财富 API → 4078.65
  └─ 用户自定义 API → 4078.62（可选）
      ↓ 交叉验证
  结果：4078.64（多数一致，可信度高）
```

### 配置示例

#### 方法1：环境变量

```bash
# Yahoo Finance（美股、日韩）
export YAHOO_API_KEY="your_api_key_here"

# Alpha Vantage（外汇、商品）
export ALPHA_VANTAGE_KEY="your_api_key_here"

# HTTP代理（访问被墙数据源）
export HTTP_PROXY="http://127.0.0.1:7890"
```

#### 方法2：配置文件

```yaml
# ~/.config/stock-toolkit/config.yaml
datasources:
  yahoo_finance:
    api_key: "your_api_key_here"
    enabled: true
  
  alpha_vantage:
    api_key: "your_api_key_here"
    enabled: true
  
  proxy:
    http: "http://127.0.0.1:7890"
    https: "http://127.0.0.1:7890"

  # 自定义数据源
  custom:
    name: "我的行情API"
    base_url: "https://your-api.com"
    api_key: "your_key"
    enabled: true
```

---

## 🚀 快速开始

### 不配置任何东西（使用免费数据源）

```bash
# 查看A股指数
python scripts/stock_toolkit.py --action indices

# 查看港股恒生指数
python scripts/stock_toolkit.py --action hsi

# 查看贵金属
python scripts/stock_toolkit.py --action precious

# 添加自选股
python scripts/stock_toolkit.py --action add_watchlist --code sh600519 --name 贵州茅台

# 查看个股详情
python scripts/stock_toolkit.py --action stock_detail --code sh600519

# 税费计算
python scripts/stock_toolkit.py --action calc_tax --buy_price 1800 --sell_price 1850 --volume 100

# 📰 个股新闻 + 情感分析（NEW）
python scripts/stock_toolkit.py --action stock_news --code sh600519 --name 贵州茅台

# 📰 板块新闻 + 情感分析
python scripts/stock_toolkit.py --action sector_news --name 新能源

# 📰 政策新闻 + 情感分析
python scripts/stock_toolkit.py --action policy_news

# 📰 市场整体情绪
python scripts/stock_toolkit.py --action market_sentiment
```

### 配置扩展数据源后

```bash
# 配置Yahoo Finance
export YAHOO_API_KEY=xxx

# 查看美股指数
python scripts/stock_toolkit.py --action us_indices

# 查看日韩指数
python scripts/stock_toolkit.py --action asia_indices
```

---

## 🖥️ 图形界面

安装后自动生成HTML仪表盘，支持：
- 🌍 **多市场切换**：A股 / 港股 / 美股 / 贵金属
- 📊 **大盘看板**：实时指数卡片
- ⭐ **自选股列表**：一键添加/删除
- 📈 **个股详情**：点击查看多维度分析
- 🧮 **税费计算**：自动代入价格计算
- 🔴🟢 **红涨绿跌**：符合A股习惯
- 📱 **响应式布局**：手机/电脑都能用
- 🔒 **零CDN依赖**：离线可用
- 🎨 **暗色主题**：护眼舒适

---

## 📦 安装

```bash
skillhub install china-stock-toolkit
```

---

## 🌟 特色

- 🌍 **全球市场** — A股/港股/美股/日韩/贵金属
- 🔄 **多源聚合** — 腾讯/新浪/东方财富三路数据
- ✅ **交叉验证** — 自动校验数据可靠性
- 🚀 **开箱即用** — 免费数据源无需配置
- 🔌 **可扩展** — 支持自定义付费数据源
- ⭐ **自选股** — 个性化关注列表
- 📈 **个股详情** — 多维度深度分析
- 🧮 **税费计算** — 精确计算交易成本
- 📊 **图形界面** — HTML仪表盘开箱即用
- 🔒 **免费** — 无需API Key即可使用基础功能
- 🇨🇳 **A股特色** — 红涨绿跌、涨跌停、北向资金

---

## 📝 更新日志

### v3.0.0 (2026-04-28)
- ✨ 新增全球市场支持（港股、美股、日韩）
- ✨ 新增贵金属行情（黄金、白银）
- ✨ 新增自选股管理功能
- ✨ 新增个股详情分析（多维度）
- ✨ 新增可扩展数据源架构
- 🐛 修复税费计算逻辑
- 📚 完善数据源配置文档

### v1.0.0 (2026-04-27)
- 🎉 首次发布
- ✅ A股5大指数
- ✅ 涨跌停监控
- ✅ 北向资金
- ✅ 税费计算器

---

*再次提醒：本工具仅供学习研究，不构成任何投资建议。投资有风险，入市需谨慎。*
