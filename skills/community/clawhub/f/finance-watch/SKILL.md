---
name: 盯盘哨兵
description: 实时盯盘工具，帮助上班族工作时间查询股票、贵金属价格走势并推送到指定频道
tags: [股票, 盯盘, 财经, 推送, 实时]
icon: 📈
author: 小妹
version: "1.3.0"
---

# 盯盘哨兵

上班族工作时间无法盯盘？让小妹帮你实时查询股票、贵金属价格走势，推送到你的频道！

## 触发场景

当用户说以下内容时触发：
- "查一下 XXX 股票"
- "看看 XXX 现在什么价格"
- "盯一下 XXX 的走势"
- "帮我看看 XXX 现在怎么样"
- "XXX 股票现在多少钱"
- "黄金/白银现在什么价格"
- "查一下原油期货"
- "看看铜的价格"
- "螺纹钢现在多少钱"
- "上证指数现在多少点"

## 支持的品种

### 股票
- **A股**：支持股票名称或代码（如"茅台"、"600519"、"贵州茅台"）
- **港股**：支持港股代码（如"00700"、"腾讯"）
- **美股**：支持美股代码（如"AAPL"、"特斯拉"）

### 贵金属
- **黄金**（AU）：现货黄金、黄金期货、黄金T+D
- **白银**（AG）：现货白银、白银期货、白银T+D
- **铂金**（PT）：铂金期货
- **钯金**（PD）：钯金期货

### 期货
- **能源期货**：原油、天然气、燃油、沥青
- **金属期货**：铜、铝、锌、铅、镍、锡
- **化工期货**：PTA、甲醇、塑料、PP、PVC
- **农产品期货**：豆粕、玉米、小麦、棉花、白糖
- **黑色系期货**：螺纹钢、热卷、铁矿石、焦炭、焦煤

### 贵金属现货
- **国际现货**：伦敦金、伦敦银
- **国内现货**：黄金T+D、白银T+D

### 指数
- **A股指数**：上证指数、深证成指、创业板指、科创50
- **港股指数**：恒生指数、恒生科技指数
- **美股指数**：道琼斯、纳斯达克、标普500

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  盯盘哨兵工作流程                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1️⃣ 解析用户请求                                             │
│     识别品种类型和代码/名称                                   │
│     股票/贵金属/期货/指数                                     │
│                                                              │
│  2️⃣ 查找品种代码                                             │
│     名称 → 标准代码（如"黄金" → "AU"）                       │
│     如果找不到，询问用户确认                                  │
│                                                              │
│  3️⃣ 选择数据源                                               │
│     根据品种类型选择合适的财经网站                            │
│     股票 → 东方财富/新浪财经                                  │
│     期货 → 东方财富期货/文华财经                              │
│     贵金属 → 东方财富                                        │
│                                                              │
│  4️⃣ 访问财经网站（必须使用 browser_use）                     │
│     步骤：                                                   │
│     - browser_use action=open url=目标URL                    │
│     - browser_use action=snapshot 获取页面数据                │
│     - 从 snapshot 中提取价格信息                              │
│                                                              │
│  5️⃣ 获取实时数据                                             │
│     - 当前价格                                               │
│     - 涨跌幅/涨跌额                                          │
│     - 今开/昨收                                              │
│     - 成交量/成交额                                          │
│     - 最高/最低                                              │
│     - 持仓量（如有）                                          │
│                                                              │
│  6️⃣ 生成分析报告                                             │
│     按照输出模板生成简洁易读的报告                            │
│                                                              │
│  7️⃣ 推送到频道                                               │
│     使用 copaw channels send 推送到用户微信                  │
│     目标：session_id=weixin:o9cq8012x7_zwZtDYePv8bo7qxLM    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 常用 URL 速查

#### 贵金属（东方财富）
| 品种 | URL | 说明 |
|------|-----|------|
| **国际黄金** | https://quote.eastmoney.com/globalfuture/GC00Y.html | COMEX黄金 |
| **沪金期货** | https://quote.eastmoney.com/qihuo/aum.html | 沪金主连 |
| **沪银期货** | https://quote.eastmoney.com/qihuo/agm.html | 沪银主连 |

#### 大宗商品（TradingEconomics）
| 品种 | URL | 说明 |
|------|-----|------|
| **商品总览** | https://zh.tradingeconomics.com/commodities | 所有商品价格一览 |
| **原油** | https://zh.tradingeconomics.com/commodity/crude-oil | WTI原油 |
| **布伦特原油** | https://zh.tradingeconomics.com/commodity/brent-crude-oil | 布伦特原油 |
| **天然气** | https://zh.tradingeconomics.com/commodity/natural-gas | 天然气 |
| **铜** | https://zh.tradingeconomics.com/commodity/copper | LME铜 |
| **铝** | https://zh.tradingeconomics.com/commodity/aluminum | LME铝 |

#### 指数（东方财富）
| 品种 | URL | 说明 |
|------|-----|------|
| **上证指数** | https://quote.eastmoney.com/sh000001.html | 上证指数 |
| **创业板指** | https://quote.eastmoney.com/sz399006.html | 创业板指 |
| **科创50** | https://quote.eastmoney.com/kcb/000688.html | 科创50 |

### A股股票 URL 拼接规则

```
基础 URL：https://quote.eastmoney.com/{市场}/{代码}.html

市场代码：
- 沪市A股：sh (如 600519)
- 深市A股：sz (如 000001)
- 创业板：sz (如 300750)
- 科创板：kcb (如 688813)
- 北交所：bj (如 872926)

示例：
- 贵州茅台：https://quote.eastmoney.com/sh600519.html
- 宁德时代：https://quote.eastmoney.com/sz300750.html
- 科创50：https://quote.eastmoney.com/kcb/000688.html
```

### 港股股票 URL 拼接规则

```
基础 URL：https://quote.eastmoney.com/hk/{代码}.html

示例：
- 腾讯控股：https://quote.eastmoney.com/hk/00700.html
- 阿里巴巴：https://quote.eastmoney.com/hk/09988.html
```

### 美股股票 URL 拼接规则

```
基础 URL：https://quote.eastmoney.com/us/{代码}.html

示例：
- 苹果：https://quote.eastmoney.com/us/AAPL.html
- 特斯拉：https://quote.eastmoney.com/us/TSLA.html
```

### 黄金查询完整示例

```
# 步骤 1: 打开国际黄金页面
browser_use action=open url=https://quote.eastmoney.com/globalfuture/GC00Y.html

# 步骤 2: 获取页面数据
browser_use action=snapshot

# 步骤 3: 提取数据（从 snapshot 结果中找）
# 当前价格、涨跌幅、今开、昨收、最高、最低、成交量

# 步骤 4（可选）: 打开沪金期货页面对比
browser_use action=open url=https://quote.eastmoney.com/qihuo/aum.html
browser_use action=snapshot
```

### 股票查询完整示例

```
# 步骤 1: 根据股票名称搜索代码
# 用户说"查一下茅台"，先确定代码是 600519

# 步骤 2: 拼接 URL 并打开
browser_use action=open url=https://quote.eastmoney.com/sh600519.html

# 步骤 3: 获取页面数据
browser_use action=snapshot

# 步骤 4: 提取数据
# 当前价格、涨跌幅、今开、昨收、最高、最低、成交量、成交额
```

### 大宗商品查询示例（原油、铜等）

**注意：TradingEconomics 网站 browser_use 无法直接访问，需用 curl 命令获取数据**

```
# 原油查询
curl -s -A "Mozilla/5.0" "https://zh.tradingeconomics.com/commodity/crude-oil" | grep -oP 'content="[^"]*原油[^"]*"'

# 从返回的 meta description 中提取：
# - 当前价格：106.33 美元/桶
# - 涨跌幅：+6.72%
# - 月涨跌幅：+49.28%

# 常用商品 URL：
# - 原油：https://zh.tradingeconomics.com/commodity/crude-oil
# - 布伦特原油：https://zh.tradingeconomics.com/commodity/brent-crude-oil
# - 天然气：https://zh.tradingeconomics.com/commodity/natural-gas
# - 铜：https://zh.tradingeconomics.com/commodity/copper
# - 铝：https://zh.tradingeconomics.com/commodity/aluminum
```

## 数据来源

### 优先级排序

1. **东方财富网** (https://quote.eastmoney.com/)
   - 数据最全，更新最快
   - 支持 A股、港股、美股、基金

2. **新浪财经** (https://finance.sina.com.cn/)
   - 备用数据源
   - 支持股票、期货、贵金属

3. **雪球** (https://xueqiu.com/)
   - 备用数据源
   - 用户讨论丰富

### URL 模板

#### 股票
```
东方财富 A股：https://quote.eastmoney.com/sh{code}.html
东方财富 港股：https://quote.eastmoney.com/hk/{code}.html
东方财富 美股：https://quote.eastmoney.com/us/{code}.html
新浪财经：https://finance.sina.com.cn/realstock/company/{code}/nc.shtml
```

#### 期货
```
东方财富期货：https://quote.eastmoney.com/inner/{code}.html
文华财经：http://quote.wenhua.com.cn/{code}.html
```

#### 贵金属
```
上海黄金交易所：https://www.sge.com.cn/
金投网黄金：https://www.cngold.org/futures/au.html
金投网白银：https://www.cngold.org/futures/ag.html
```

#### 指数
```
东方财富指数：https://quote.eastmoney.com/center/gridlist.html#index
上证指数：https://quote.eastmoney.com/sh000001.html
深证成指：https://quote.eastmoney.com/sz399001.html
```

## 输出模板

### 黄金简报（国际+国内）

**查询黄金时必须同时获取国际金价和国内金价！**

```
📊 【黄金市场简报】{日期}

【国际金价】COMEX黄金
最新价：{国际价格} 美元/盎司
涨跌幅：{国际涨跌幅}%（+{国际涨跌额}美元）
今日区间：{国际最低} - {国际最高}

【国内金价】沪金主连
最新价：{国内价格} 元/克
涨跌幅：{国内涨跌幅}%（+{国内涨跌额}元）
今日区间：{国内最低} - {国内最高}

【分析】
{简要分析}

更新时间：{时间}
```

**推送格式要求**：
- 标题带emoji（如📊）
- 使用中文方括号
- 每行内容完整显示
- 包含国际金价（COMEX黄金）和国内金价（沪金主连）

### 原油简报（国际+国内）

**查询原油时必须同时获取国际油价和国内油价！**

```
📊 【原油市场简报】{日期}

【国际油价】WTI原油
最新价：{国际价格} 美元/桶
涨跌幅：{国际涨跌幅}%（{国际涨跌额}美元）
今日区间：{国际最低} - {国际最高}

【国内油价】SC原油
最新价：{国内价格} 元/桶
涨跌幅：{国内涨跌幅}%（{国内涨跌额}元）
今日区间：{国内最低} - {国内最高}

【分析】
{简要分析}

更新时间：{时间}
```

### 股票简报

```
📊 【{股票名称} {代码}】实时行情

💰 现价：{价格} 元
📈 涨跌：{涨跌幅}% ({涨跌额}元)
📅 今开：{今开}  昨收：{昨收}
📅 最高：{最高}  最低：{最低}
📊 成交量：{成交量}手
📊 成交额：{成交额}亿元

⏰ {时间}
```

### 期货简报

```
📈 【{品种名称}】实时行情

💰 现价：{价格} 元
📈 涨跌：{涨跌幅}% ({涨跌额}元)
📅 今开：{今开}  昨结：{昨结}
📅 最高：{最高}  最低：{最低}
📊 成交量：{成交量}手
📊 持仓量：{持仓量}手

⏰ {时间}
```

## 推送配置

### 用户配置

当前用户配置（已绑定）：

```
频道：微信
target_user: o9cq8012x7_zwZtDYePv8bo7qxLM@im.wechat
target_session: weixin:o9cq8012x7_zwZtDYePv8bo7qxLM@im.wechat
```

### 推送命令模板

```bash
copaw channels send \
  --agent-id default \
  --channel wechat \
  --target-user "o9cq8012x7_zwZtDYePv8bo7qxLM@im.wechat" \
  --target-session "weixin:o9cq8012x7_zwZtDYePv8bo7qxLM@im.wechat" \
  --text "{简报内容}"
```

## 常用股票代码速查

| 股票名称 | 代码 | 市场 |
|---------|------|------|
| 贵州茅台 | 600519 | A股 |
| 宁德时代 | 300750 | A股 |
| 比亚迪 | 002594 | A股 |
| 腾讯控股 | 00700 | 港股 |
| 阿里巴巴 | 09988 | 港股 |
| 特斯拉 | TSLA | 美股 |
| 苹果 | AAPL | 美股 |
| 英伟达 | NVDA | 美股 |

## 注意事项

1. **数据延迟**：财经网站数据可能有 1-3 分钟延迟
2. **访问频率**：避免频繁访问同一网站，建议间隔 1 分钟以上
3. **非交易时间**：非交易时间显示的是收盘价
4. **风险提示**：仅供参考，不构成投资建议

## 示例对话

### 示例 1：查询 A股

```
用户：查一下茅台现在怎么样

小妹：
📊 【贵州茅台 600519】实时行情

💰 当前价格：1688.00 元
📈 涨跌幅：+2.35% (+38.68元)
📅 今日区间：1650.00 - 1695.50
📊 成交量：15234手
💵 成交额：25.68亿

💡 简要分析：
今日走势较强，成交量放大，资金流入明显。

⏰ 查询时间：2026-03-31 14:30:00

已推送到您的微信频道 ✅
```

### 示例 2：查询黄金（国际+国内）

```
用户：看看黄金现在什么价格

小妹：打开国际黄金和沪金页面，获取数据，推送简报

【黄金市场简报】2026-03-31

【国际金价】COMEX黄金
最新价：4589.30 美元/盎司
涨跌幅：+0.70%（+31.80美元）
今日区间：4510.00 - 4649.50

【国内金价】沪金主连
最新价：1020.10 元/克
涨跌幅：+0.52%（+5.22元）
今日区间：1011.00 - 1034.20（创新高）

【分析】
国际金价避险情绪推动，美元走弱支撑
沪金创出新高1034.20，技术面强势

更新时间：19:05

已推送到您的微信频道 ✅
```

### 示例 3：查询期货

```
用户：查一下螺纹钢期货

小妹：
📈 【螺纹钢 RB2405】实时行情

💰 当前价格：3650 元/吨
📈 涨跌幅：-1.23%
📅 今日区间：3620 - 3700
📊 成交量：125,680手
💵 持仓量：1,256,890手
📅 昨日结算：3695元

💡 简要分析：
【震荡偏弱】受需求淡季影响，螺纹钢震荡下行，关注3600支撑。

⏰ 查询时间：2026-03-31 14:30:00

已推送到您的微信频道 ✅
```

### 示例 4：查询指数

```
用户：大盘现在怎么样

小妹：
📊 【上证指数】实时行情

💰 当前点位：3088.56
📈 涨跌幅：+0.85%
📅 今日区间：3065.23 - 3098.12
📊 成交额：3256亿

💡 简要分析：
【震荡上行】大盘今日放量上涨，权重股表现活跃，量能配合良好。

⏰ 查询时间：2026-03-31 14:30:00

已推送到您的微信频道 ✅
```

### 示例 5：查询港股

```
用户：看看腾讯现在多少钱

小妹：
📊 【腾讯控股 00700】实时行情

💰 当前价格：368.80 港元
📈 涨跌幅：+1.56%
📅 今日区间：365.00 - 372.40
📊 成交量：15,234,000股
💵 成交额：56.2亿港元

💡 简要分析：
【震荡上行】腾讯今日放量上涨，游戏业务利好消息刺激。

---

## 变更记录

| 日期 | 版本 | 修改内容 |
|------|------|---------|
| 2026-03-31 | 1.4.0 | 固化黄金简报模板，添加原油模板，使用emoji格式，已发布到ClawHub |
| 2026-03-31 | 1.3.0 | 新增TradingEconomics大宗商品数据源、curl查询方式 |
| 2026-03-31 | 1.2.0 | 新增国际黄金URL、A股股票URL拼接规则、简化输出模板 |
| 2026-03-31 | 1.1.0 | 新增browser_use抓取流程、常用URL速查、推送命令模板 |
| 2026-03-31 | 1.0.0 | 初始版本 |
