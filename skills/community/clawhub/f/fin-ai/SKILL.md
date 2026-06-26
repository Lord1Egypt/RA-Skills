---
name: fin-ai
description: 中文投资组合管理 skill：同步持仓、基于 holdings 重算组合结果、生成当日 snapshot/history。适用于用户提供截图、CSV、券商导出或 holdings-like JSON，需要更新持仓、刷新组合结果、检查 warnings、落盘快照时。
---

# fin-ai

当用户要做下面这些事时使用这个 skill：

- 同步或更新持仓
- 基于当前 holdings 重算组合结果
- 生成或刷新某一天的 snapshot / history
- 检查本次运行的 warnings
- 第一次为用户初始化投资组合数据目录

## 首次使用引导

如果这是用户第一次使用这个 skill，优先用自然语言确认一件事：

- 使用默认数据目录
- 或者使用用户提供的自定义目录

默认情况下，优先推荐默认数据目录。
只有用户已经有现成的数据目录，或者明确希望自己管理路径时，再使用自定义目录。

如果用户没有可用数据目录，就先初始化目录，再继续后续 workflow。

## 写操作确认规则

凡是会改动真实数据目录的操作，默认都先预演：

- 导入或更新持仓
- 刷新并落盘当日 snapshot / history
- 任何会改动 `holdings` / `snapshots` / `history.csv` 的动作

预演时：
- 结果直接展示在对话里（用户可读的摘要：总资产、盈亏、账户组、warnings）
- 不写临时文件，不生成临时文件路径
- 用户确认后再写入真实持久目录

正式写入：
- 用户在对话里明确确认后，执行真实写入
- 写入结果再次展示给用户确认

## 默认使用方式

- 如果用户给了新的持仓数据：
  先同步 holdings，再重算结果，再落 snapshot
- 如果用户没有给新持仓：
  直接基于现有 holdings 重算并落 snapshot

第一次使用时，先确认用户希望：
- 使用默认数据目录
- 还是提供一个自定义数据目录

默认数据目录在：
`~/.agents/data/portfolio-workflows/<profile>/portfolio`

这个默认路径会记录在用户配置文件里：
`~/.agents/data/portfolio-workflows/settings.json`

后续如果用户没有显式提供路径，就直接用配置文件里的默认目录。

除非用户明确要求，否则不要主动向用户解释脚本路径、repo 结构或内部文件布局。
对用户只需要表达：
- 当前使用哪个数据目录
- 是否会改真实数据
- 本次会执行哪类动作（同步持仓 / 重算 / 落快照）
- 默认优先返回用户摘要，不主动暴露完整内部 JSON

同步持仓时，默认按“账户组替换”理解。
只有用户明确说“整份覆盖今天持仓”时，才应该走整份覆盖模式。

## 关键规则

- `holdings` 是真源
- `snapshot` 是派生结果，不是真源
- 默认不要直接改真实数据，预演结果直接展示给用户确认后再写入
- 正式发布态的数据目录应放在 repo 外
- 用户可以提供自定义路径；如果没提供，就用默认目录或配置文件里的目录
- 只有在用户明确要整份覆盖当天持仓时，才使用整份覆盖模式

## 外部行情源注入（可选）

Agent 可主动调用外部 CLI（如 ticker）获取行情，再注入到分析流程：

1. 调用 ticker CLI：`ticker --config <config> print --format json`
2. 转换为 market_context.json（格式见下）
3. 调用 `portfolio_analysis.py --market-context /path/to/market_context.json`
4. 缺失标的由内置 HTTP source 补齐

**market_context.json 格式：**
```json
{
  "prices": {"NASDAQ:AMZN": 262.59, "OTC:002963": 3.20},
  "currencies": {"NASDAQ:AMZN": "USD", "OTC:002963": "CNY"},
  "fx_rates": {"CNY": 1.0, "USD": 6.8, "HKD": 0.87},
  "warnings": [],
  "meta": {}
}
```

**ticker config 示例（/tmp/ticker.yaml）：**
```yaml
watchlist:
  - AMZN
  - BIL
  - DIA
  - QQQ
  - QQQM
  - SCHD
  - SGOV
  - SOXX
  - VOO
  - VXUS
  - NIO
lots:
  - symbol: AMZN
    quantity: 1
    unit_cost: 1
  # ... 每个 symbol 都需要一个 synthetic lot
```

**merge 规则：**
- 外部 prices/currencies/fx_rates 优先
- 缺失标的由内置 source 补齐并写入 warning
- OTC 基金始终由内置 source 处理（ticker 不支持 OTC）

**调用示例：**
```bash
# 1. 获取 ticker 价格并生成 market_context.json
ticker --config /tmp/ticker.yaml print --format json | \
  jq '{prices: (map({key: ("NASDAQ:" + .symbol), value: (.price | tonumber)}) | from_entries),
      currencies: (map({key: ("NASDAQ:" + .symbol), value: "USD"}) | from_entries),
      fx_rates: {"CNY": 1.0, "USD": 6.8},
      warnings: [], meta: {}}' > /tmp/market-context.json

# 2. 注入到分析流程
python3 scripts/portfolio_analysis.py \
  --date 2026-05-16 \
  --portfolio-dir ~/.agents/data/portfolio-workflows/default/portfolio \
  --market-context /tmp/market-context.json
```

## CLI 调用语法

### refresh_portfolio.py（主入口）

```bash
python3 scripts/refresh_portfolio.py \
  --date 2026-05-16 \
  --portfolio-dir ~/.agents/data/portfolio-workflows/default/portfolio \
  [--confirm-write] \
  [--skip-history] \
  [--output-format summary|debug]
```

| 参数 | 说明 |
|------|------|
| `--date` | 目标日期，格式 YYYY-MM-DD |
| `--portfolio-dir` | 数据目录，不提供则使用默认或 profile 目录 |
| `--profile` | 用户数据 profile 名，默认 default |
| `--confirm-write` | 确认写入真实目录；未提供则默认预演（不写真实文件） |
| `--skip-history` | 跳过 history.csv 更新 |
| `--output-format` | summary=用户可读摘要；debug=完整 JSON |

### portfolio_analysis.py（分析）

```bash
python3 scripts/portfolio_analysis.py \
  --date 2026-05-16 \
  --portfolio-dir ~/.agents/data/portfolio-workflows/default/portfolio \
  [--market-context /path/to/market_context.json] \
  [--output /path/to/output.json]
```

| 参数 | 说明 |
|------|------|
| `--date` | 目标日期，格式 YYYY-MM-DD |
| `--portfolio-dir` | 数据目录 |
| `--profile` | 用户数据 profile 名，默认 default |
| `--market-context` | 外部 market_context JSON；提供后跳过内置 HTTP 获取 |
| `--output` | 可选输出路径 |

### holdings_sync.py（同步）

```bash
python3 scripts/holdings_sync.py \
  --input '{"groups": {...}}' \
  --portfolio-dir ~/.agents/data/portfolio-workflows/default/portfolio \
  --date 2026-05-16
```

| 参数 | 说明 |
|------|------|
| `--input` | holdings-like JSON payload |
| `--portfolio-dir` | 数据目录 |
| `--date` | 目标日期 |

### persist_snapshot.py（落盘）

```bash
python3 scripts/persist_snapshot.py \
  --analysis-result /path/to/analysis.json \
  --date 2026-05-16 \
  --portfolio-dir ~/.agents/data/portfolio-workflows/default/portfolio
```

| 参数 | 说明 |
|------|------|
| `--analysis-result` | portfolio_analysis 输出 JSON |
| `--date` | 目标日期 |
| `--portfolio-dir` | 数据目录 |

## Warning 类型

系统会产生以下类型的 warning：

### 数据获取类
| Warning | 含义 | 处理方式 |
|---------|------|----------|
| `XXX 当日估值不可用，已回退为最近披露净值` | OTC 基金当天净值获取失败，使用历史数据 | 正常，可接受 |
| `XXX Yahoo 价格获取失败，已回退为 stooq 报价` | Yahoo 获取失败，stooq 回退成功 | 正常，可接受 |
| `XXX 当前价格获取失败，已回退为 0` | 所有数据源都失败，回退到 0 | 需要关注，可能数据有问题 |

### 汇率类
| Warning | 含义 | 处理方式 |
|---------|------|----------|
| `HKD 汇率获取失败，已回退为 0.88` | 无法获取 HKD/CNY，使用默认汇率 | 正常，可接受 |
| `USD 汇率获取失败，已回退为 6.90` | 无法获取 USD/CNY，使用默认汇率 | 正常，可接受 |

### 持仓数据类
| Warning | 含义 | 处理方式 |
|---------|------|----------|
| `XXX 的 cost_price 为 0，收益率可能失真` | 持仓成本为 0 | 需要用户确认是否正常 |
| `XXX 使用未知币种 XXX，汇率已回退为 1.0` | 币种无法识别 | 需要检查 ticker 配置 |

### 外部注入类
| Warning | 含义 | 处理方式 |
|---------|------|----------|
| `外部 market_context 缺少 N 个标的，已使用内置 source 补齐` | 外部 context 未覆盖全部标的 | 正常，缺失部分由内置补齐 |
| `market_context 仍缺少 N 个标的` | 即使内置补齐后仍有缺失 | 需要关注 |

## 何时读参考资料
- 涉及 lot 明细：
  读 [references/schema-lots.md](references/schema-lots.md)
- 改分析输出或 snapshot 落盘：
  读 [references/schema-snapshot.md](references/schema-snapshot.md)
- 改 workflow 边界或输入输出 contract：
  读 [references/workflow-contracts.md](references/workflow-contracts.md)
