---
name: daxiapi
description: '大虾皮(daxiapi.com)金融数据API服务入口，负责路由分发到具体分析skill。触发词：A股数据、市场数据、股票分析、板块分析、选股、市场复盘、财务分析、财报分析、ROE分析、杜邦分析、个股舆情、公告解读、研报解读、主力资金、资金流向、资金动向。适用场景：获取A股市场、板块、个股、财报、消息面、资金流向数据时的统一入口，根据用户需求分发到对应的专业skill。不适用场景：非A股市场分析、非金融数据分析、纯技术问答。'
---

# 大虾皮 API 路由 Skill

大虾皮(daxiapi.com)提供专业的A股量化数据API服务，本skill作为统一入口，负责识别用户意图并路由分发到具体分析skill。

## Overview（功能概述）

识别用户的金融数据分析需求，智能匹配并调用对应的专业skill，确保分析质量和效率。如果已有明确的专业skill覆盖用户需求，则直接调用该skill；否则提供通用CLI命令供用户使用。

## When to Use（何时使用）

当用户请求以下数据时，触发此skill进行路由分发：

- A股市场相关数据查询
- 板块、行业分析需求
- 股票筛选和选股需求
- 市场情绪、温度、估值分析
- 风格轮动、大小盘分析
- 个股财务分析、财报分析、ROE/杜邦分析
- 个股舆情、公告、研报等消息面分析
- 个股主力资金流向、个股资金动向分析

**具体触发词**：A股数据、市场数据、股票分析、板块分析、选股、市场复盘、财务分析、财报分析、ROE分析、杜邦分析、个股舆情、公告解读、研报解读、消息面分析、个股主力资金、个股资金流向、个股资金动向   

## When Not to Use（何时不使用）

以下场景不应使用本Skill：

- 非A股市场分析（美股、港股、债券、基金、期货等）
- 非金融数据分析需求
- 纯技术问答或编程问题
- 理论知识讲解（如"什么是EMA"）

## Process（流程主体）

### Step 1: 意图识别与路由分发

**目标**：识别用户的具体需求，匹配对应的专业skill

**路由映射表**：

| 用户需求关键词 | 匹配Skill | 说明 |
|--------------|-----------|------|
| 市场复盘、今天市场怎么样、市场分析、每日复盘 | `xiapi-market-review` | 综合市场复盘 |
| 市场温度、市场估值、恐贪指数、市场情绪、趋势温度、动量温度 | `xiapi-market-temperature` | 市场温度分析（底层命令：`market temp` + `market compass`） |
| 大小盘风格、风格轮动、大盘股小盘股、风格切换 | `xiapi-style-rotation` | 风格轮动分析 |
| 板块热力图、行业轮动、热门板块、领涨板块 | `xiapi-heatmap-analysis` | 板块热力图分析 |
| 涨停、跌停、炸板、涨跌停分析 | `xiapi-price-limit-analysis` | 涨跌停分析 |
| 热门股票、领涨股、强势股、涨幅榜 | `xiapi-top-stocks` | 热门股票分析 |
| 股票筛选、选股、VCP形态、RPS强势股、创新高、技术形态 | `xiapi-screener` | 技术形态选股 |
| SQL选股、选股、股票筛选、技术筛选、量化筛选、自定义筛选、条件选股 | `xiapi-stock-sql-screener` | SQL条件选股（自定义多条件组合筛选） |
| 个股分析、个股对比、财报对比、价值分析、技术分析、基本面、买卖点、选时、ST分析 | `xiapi-stock-analysis` | 个股深度分析与多股对比（综合/技术/财报/价值） |
| 财务分析、财报分析、ROE分析、杜邦分析、盈利质量、净利润质量、`report finance` | `xiapi-financial-roe-analysis` | 基于 `daxiapi report finance <code>` 的个股财务深度分析 |
| 个股舆情、公告解读、研报解读、消息面分析、新闻催化、利好利空、`news sentiment`、`news notice`、`news report` | `xiapi-news-catalyst-analysis` | 基于 `daxiapi news` 的个股消息面交叉验证与影响评分分析 |
| 红利指数、红利分析、中证红利、红利低波、股息率指数 | `xiapi-dividend-analysis` | 红利指数分析 |
| 个股主力资金、个股资金流向、个股主力净流入、个股资金动向 | 通用CLI命令 | 使用 `daxiapi stock capital-flow <code>` 获取个股主力资金流向 |

**路由判断流程**：

1. **扫描关键词**：从用户输入中提取关键词
2. **匹配Skill**：根据路由映射表匹配对应skill
3. **优先匹配专业skill**：
   - 若出现"财务分析/财报分析/ROE/杜邦/盈利质量"等意图，优先路由到 `xiapi-financial-roe-analysis`
   - 若出现"舆情/公告/研报/消息面/利好利空/新闻催化"等意图，优先路由到 `xiapi-news-catalyst-analysis`
   - 若出现"个股分析/个股对比/技术分析/价值分析/基本面/买卖点"等意图，优先路由到 `xiapi-stock-analysis`
   - 若出现"个股主力资金/个股资金流向/个股主力净流入/个股资金动向"等意图，提供CLI命令 `daxiapi stock capital-flow <code>`
4. **直接调用**：找到匹配skill后，直接调用该skill执行分析
5. **无匹配处理**：如无明确匹配，进入Step 2通用处理

**示例**：

```
用户输入："分析一下红利低波指数"
匹配结果：关键词包含"红利低波" → 调用 `xiapi-dividend-analysis`

用户输入："今天涨停板有哪些？"
匹配结果：关键词包含"涨停" → 调用 `xiapi-price-limit-analysis`

用户输入："帮我选一些VCP形态的股票"
匹配结果：关键词包含"VCP形态"、"选股" → 调用 `xiapi-screener`

用户输入："分析一下宁德时代的财务质量"
匹配结果：关键词包含"财务质量"、"财务分析" → 调用 `xiapi-financial-roe-analysis`

用户输入："用 report finance 看一下 300750 的 ROE 和盈利质量"
匹配结果：关键词包含"report finance"、"ROE"、"盈利质量" → 调用 `xiapi-financial-roe-analysis`

用户输入："帮我看下 600031 最近舆情、公告和研报，判断利好利空"
匹配结果：关键词包含"舆情"、"公告"、"研报"、"利好利空" → 调用 `xiapi-news-catalyst-analysis`

用户输入："帮我分析一下宁德时代和比亚迪，哪个更值得持有"
匹配结果：关键词包含"个股对比"、"值得持有" → 调用 `xiapi-stock-analysis`

用户输入："三一重工现在技术面怎么样，适合买入吗"
匹配结果：关键词包含"技术面"、"买入" → 调用 `xiapi-stock-analysis`
```

---

### Step 2: 通用处理（无明确匹配时）

**触发条件**：用户需求无法匹配到具体skill

**处理方式**：

1. **提供CLI命令**：直接提供对应的CLI命令供用户使用
2. **说明数据范围**：告知用户该命令能获取的数据类型
3. **优先补充路由提示**：如果用户已表现出分析意图，不只给命令，要优先引导到对应skill
4. **引导到相关skill**：如有相关skill，推荐用户使用

**CLI 命令速查表**：

### 配置管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `config set <key> <value>` | 设置配置项 | `daxiapi config set token YOUR_TOKEN` |
| `config get` | 查看所有配置 | `daxiapi config get` |
| `config delete <key>` | 删除配置项 | `daxiapi config delete token` |

### 市场数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `market index` | 获取A股市场主流指数数据（上证指数、深证成指、沪深300、上证50、中证500、创业板指、科创50等） | `daxiapi market index` |
| `market compass` | 获取市场三维结构综合判断（趋势+估值+情绪），**推荐优先使用** | `daxiapi market compass` |
| `market temp` | 获取市场温度原始数据（估值温度、恐贪指数、趋势温度、动量温度），compass 的数据来源 | `daxiapi market temp` |
| `market style` | 获取A股市场风格数据（大小盘风格轮动） | `daxiapi market style` |
| `market value` | 获取A股主要指数估值数据（PE、PB、估值温度、百分位等） | `daxiapi market value` |

### 板块数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `sector heatmap` | 获取A股板块热力图数据（支持按强度、涨跌幅排序） | `daxiapi sector heatmap --order cs --limit 5` |
| `sector bk` | 获取A股行业板块数据（同花顺分类） | `daxiapi sector bk` |
| `sector stocks` | 获取A股指定板块内股票排名（支持多维度排序） | `daxiapi sector stocks --code BK0428 --order cs` |
| `sector top` | 获取A股热门股票数据（涨幅>7%且IBS>50） | `daxiapi sector top` |
| `sector gn` | 获取A股热门概念板块列表 | `daxiapi sector gn --type ths` |

### 个股数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `stock info <codes...>` | 根据股票代码获取详细信息（支持批量，最多20只；`--mode intraday` 查询盘中快照） | `daxiapi stock info 000001 600031 300750` |
| `stock gn <gnId>` | 根据概念板块ID获取该概念下的所有股票 | `daxiapi stock gn GN1234 --type ths` |
| `stock pattern <pattern>` | 根据技术形态筛选股票（支持27种形态；`--mode intraday` 查询盘中选股） | `daxiapi stock pattern vcp` |
| `stock capital-flow <code>` | 获取个股主力资金流向（默认5天，最多30天） | `daxiapi stock capital-flow 600031 --days 10` |
| `sql <condition>` | 使用SQL条件筛选股票（支持自定义条件组合、排序和数量限制） | `daxiapi sql "date='2026-06-17' AND rps_score>70 ORDER BY rps_score DESC LIMIT 20"` |

**capital-flow 字段说明**：
- `当日资金流入`：主力当日净流入金额（正=净流入，负=净流出），单位元
- `当日资金流入占比`：主力净流入占当日成交额比例（%），反映主力参与强度
- `5日资金流入金额`：近5日主力净流入累计，判断中短期资金趋势
- `5日资金流入占比`：近5日主力净流入占比
- `板块资金流入`：所属行业板块当日主力净流入，判断板块整体资金方向
- `5日板块资金流入金额`：所属板块近5日主力净流入累计

**技术形态类型**：
- 强度指标类：`gxl`、`rps`、`sctr`、`csTop3`、`sctrTop3`、`rpsTop3`
- 趋势形态类：`trendUp`、`high_60d`、`newHigh`、`crossMa50`、`crossoverBox`
- 成交量形态类：`fangliang`、`fangliangtupo`
- 涨跌幅排名类：`zdf1dTop3`、`zdf5dTop3`、`zdf10dTop3`、`zdf20dTop3`
- 经典技术形态类：`vcp`、`joc`、`sos`、`spring`、`w`、`lps`、`sos_h1`
- 其他：`ibs`、`shizhiTop3`

### K线数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `kline <code>` | 获取A股股票、指数、板块的K线数据 | `daxiapi kline 000001` |

### 涨跌停数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `zdt` | 获取A股涨跌停股票池数据 | `daxiapi zdt --type zt` |

**类型参数**：
- `zt` - 涨停
- `dt` - 跌停
- `zb` - 炸板

### 代码转换与搜索

| 命令 | 说明 | 示例 |
|------|------|------|
| `secid <code>` | 将各种股票代码格式转换为标准secid格式 | `daxiapi secid 000001` |
| `search <keyword>` | 搜索A股股票或板块（支持模糊查询） | `daxiapi search 平安 --type stock` |

### 红利指数

| 命令 | 说明 | 示例 |
|------|------|------|
| `dividend score` | 获取红利类指数的打分数据 | `daxiapi dividend score -c 2.H30269` |

**常用指数代码**：
- `2.H30269` - 红利低波
- `2.930955` - 红利低波100
- `1.000922` - 中证红利
- `2.932365` - 中证现金流

### 热榜数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `hotrank stock` | 获取A股热股榜数据 | `daxiapi hotrank stock --type hour --list-type normal` |
| `hotrank concept` | 获取A股概念板块热榜数据 | `daxiapi hotrank concept` |
| `hotrank board` | 获取A股行业板块热榜数据 | `daxiapi hotrank board --type industry` |

**热股榜类型**：
- `normal` - 大家都在看
- `skyrocket` - 快速飙升个股
- `trend` - 趋势投资派关注个股
- `value` - 价值派关注个股
- `tech` - 技术派关注个股

### 成交额数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `turnover` | 获取A股市场成交额数据 | `daxiapi turnover` |

### 新闻数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `news sentiment` | 获取个股舆情列表（传入 `code`，内部自动转 secid） | `daxiapi news sentiment -c 600031 -p 20` |
| `news notice` | 获取个股公告列表 | `daxiapi news notice -c 600031 -p 20 -i 1` |
| `news report` | 获取个股研报列表（支持时间区间） | `daxiapi news report -c 600031 -p 25 -i 1 -b 2026-01-01 -e 2026-04-08` |

### 财报数据

| 命令 | 说明 | 示例 |
|------|------|------|
| `report finance <code>` | 获取指定股票的财务报表数据；若用户要进一步做 ROE、杜邦、盈利质量分析，应路由到 `xiapi-financial-roe-analysis` | `daxiapi report finance 300014` |

---

### Step 3: Token 配置检查（可选）

**触发条件**：用户首次使用或提示认证失败

**跳过条件**：Token已配置且有效

**执行步骤**：

**步骤 3.1：检查Token配置状态**

```bash
npx daxiapi-cli@latest config get token
```

**步骤 3.2：如未配置，获取Token**

1. 提示用户访问 [daxiapi.com](https://daxiapi.com) 个人主页
2. 开通API Token功能
3. 获取生成的Token

**步骤 3.3：配置Token**

```bash
# 方式一：通过CLI配置（推荐）
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 方式二：设置环境变量
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI
```

**步骤 3.4：验证配置**

```bash
npx daxiapi-cli@latest market
```

如返回正常市场数据，则配置成功。

## Quality Checks（质量检查）

### 路由准确性检查

| 检查项 | 说明 | 标准 |
|-------|------|------|
| ✅ 关键词匹配 | 是否正确识别用户意图关键词 | 至少匹配1个关键词 |
| ✅ Skill调用 | 是否调用了正确的skill | skill名称与需求一致 |
| ✅ 降级处理 | 无匹配时是否提供有效方案 | 提供CLI命令或引导 |

### 服务质量检查

| 检查项 | 说明 | 标准 |
|-------|------|------|
| ✅ Token状态 | 是否检查Token配置 | 首次使用时检查 |
| ✅ 错误处理 | 认证失败是否有明确提示 | 提供配置指引 |
| ✅ 用户引导 | 是否提供清晰的使用说明 | 说明数据范围和限制 |

## Common Pitfalls（常见陷阱）

| 陷阱 | 说明 | 避免方法 |
|-----|------|----------|
| 误判意图 | 将单一指标需求误判为综合分析 | 优先匹配具体skill，再考虑综合skill |
| 财务分析漏路由 | 用户已明确要求财报/ROE/杜邦分析，却只返回 `report finance` 命令 | 命中财务关键词时优先调用 `xiapi-financial-roe-analysis` |
| 重复路由 | 在路由skill和具体skill之间循环调用 | 明确区分路由层和执行层职责 |
| 忽略Token | 未检查Token配置直接调用API | 首次使用时强制检查Token状态 |

## Key Principles（重要原则）

1. **精确匹配优先**：优先匹配具体的专业skill，避免泛泛调用
2. **分析意图优先于取数意图**：比如用户一旦表达“财务分析/ROE/杜邦/盈利质量”诉求，应优先路由到 `xiapi-financial-roe-analysis`，而不是只停留在命令层
3. **避免重复分析**：不要同时调用多个有重叠功能的skill
4. **降级有方案**：无匹配skill时，提供有效的CLI命令
5. **Token透明**：首次使用时主动检查Token配置状态

## Error Handling（错误处理）

### 路由错误

**错误1：无匹配skill**

- 场景：用户需求无法匹配到任何skill
- 处理：提供相关CLI命令，说明数据范围

**错误2：多skill匹配**

- 场景：用户需求同时匹配多个skill
- 处理：选择最具体的skill，或询问用户具体需求

### 认证错误

**错误3：Token缺失或失效**

```bash
# 错误表现
401 Unauthorized
Authentication failed

# 处理方式
npx daxiapi-cli@latest config get token  # 检查配置
npx daxiapi-cli@latest config set token YOUR_TOKEN  # 重新配置
```

**错误4：请求频率超限**

```bash
# 错误表现
429 Too Many Requests

# 处理方式
等待30-60秒后重试
```

## References

详细文档请参考：

- [API参考](references/api-reference.md) - 详细API参数说明
- [字段说明](references/field-descriptions.md) - 专用名词和字段详细说明
