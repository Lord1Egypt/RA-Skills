---
name: a-share-sector
description: >-
  查询 A 股行业/概念/地域板块的涨跌与资金流向，支持当天实时与指定历史日期（--date）；
  输出涨跌幅、成交量、主力流入、主力流出，以及板块内个股详情（detail 支持 --hot 双视图）。
  数据来自东方财富（akshare）。当用户问 A股板块、行业板块、概念板块、板块涨跌、板块资金流、
  换手率、成交量、主力净流入、流入流出、某日板块表现、板块里哪些股票涨得好或资金量大时使用；
  须优先执行 scripts/query.py，禁止手写爬虫。
---

# A股板块行情查询

查询 A 股**行业/概念/地域**板块的涨跌与资金流向，以及板块内个股的成交量、成交额、换手率、主力净流入/流出。支持**当天实时**与**指定历史日期**查询。

数据来源：[东方财富](https://quote.eastmoney.com/)（通过 [akshare](https://github.com/akfamily/akshare) 获取）。**仅供研究参考，不构成投资建议。**

## 前置条件

首次使用前安装依赖（脚本也会自动尝试安装）：

```bash
pip install -r ~/.cursor/skills/a-share-sector/requirements.txt
```

需要 Python 3.9+ 与网络访问。

## 工作流

根据用户意图选择命令，**必须优先执行脚本**，**禁止**为同一需求手写 akshare 爬虫：

```bash
python ~/.cursor/skills/a-share-sector/scripts/query.py <command> [options]
```

典型组合：

1. `overview --date …` 查板块涨跌榜
2. 对每个目标板块执行 `detail --date … --hot` 查领涨 + 资金活跃个股

### 1. 板块涨跌概览（默认场景）

用户问「今天哪些板块涨/跌」「6月26日哪些板块涨了」：

```bash
# 当天实时（默认）
python ~/.cursor/skills/a-share-sector/scripts/query.py overview --type industry --top 10
python ~/.cursor/skills/a-share-sector/scripts/query.py overview --type concept --top 15

# 指定历史日期
python ~/.cursor/skills/a-share-sector/scripts/query.py overview --date 2026-06-26 --type industry --top 15
python ~/.cursor/skills/a-share-sector/scripts/query.py overview --date 20260626 --type concept --gainers-only
python ~/.cursor/skills/a-share-sector/scripts/query.py overview --date 2026-06-26 --type industry --no-flow
```

输出：涨幅榜 + 跌幅榜，含**涨跌幅、成交量、主力流入、主力流出**（历史日期默认查询资金流；加 `--no-flow` 可跳过以加速）。

**历史查询说明**：需逐板块拉取日 K，约 500 个板块需 30–60 秒；`--workers` 可调并发（默认 8）。地域板块（`region`）暂不支持历史日期。实时板块列表接口不含成交量，历史查询才有板块成交量。

### 2. 板块内个股详情

用户问某板块内「哪些股票涨得好、资金量大」，或指定日期的成份股表现：

```bash
# 当天实时
python ~/.cursor/skills/a-share-sector/scripts/query.py detail 半导体 --type concept
python ~/.cursor/skills/a-share-sector/scripts/query.py detail 银行 --type industry --sort flow --limit 20

# 历史日期：领涨 + 资金活跃（推荐）
python ~/.cursor/skills/a-share-sector/scripts/query.py detail 有机硅 --date 2026-06-26 --type industry --hot --limit 5
python ~/.cursor/skills/a-share-sector/scripts/query.py detail 航天装备 --date 20260626 --type industry --hot --limit 5

# 历史日期：按成交额排序
python ~/.cursor/skills/a-share-sector/scripts/query.py detail 半导体材料 --date 2026-06-26 --sort amount --gainers-only --limit 10
```

输出：代码、名称、涨跌幅、收盘价/最新价、**成交量**、成交额、换手率、**主力流入**、**主力流出**。

`--sort` 可选：`change`（涨跌幅）、`amount`（成交额）、`volume`（成交量）、`turnover`（换手率）、`flow`（主力净流入）。

`--hot`：同时输出「涨幅前列」+「上涨股中成交额靠前」，适合「涨得好且资金量大」类问题。

`--no-flow`：跳过主力流入/流出（查询更快）。默认会查询资金流。

**历史 detail 说明**：逐股拉取日 K，一个板块约 10–30 秒；成份股列表按**当前**板块成分回溯。主力流入/流出由东方财富「主力净流入」净值拆分，接口不提供独立 gross 流入/流出。

### 3. 板块资金流排行

用户只关心资金流入/流出：

```bash
# 当天
python ~/.cursor/skills/a-share-sector/scripts/query.py fund-flow --type industry --period 今日 --top 10

# 历史日期
python ~/.cursor/skills/a-share-sector/scripts/query.py fund-flow --date 2026-06-26 --type industry --top 10
```

### 4. 列出板块名称

用户不确定板块叫什么，或需要模糊匹配前先看列表（**仅支持当天**）：

```bash
python ~/.cursor/skills/a-share-sector/scripts/query.py list --type industry
python ~/.cursor/skills/a-share-sector/scripts/query.py list --type concept
```

## 参数说明

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `--date` | `YYYY-MM-DD` / `YYYYMMDD` | 指定查询日期；省略则查当天实时 |
| `--type` | `industry` / `concept` / `region` | 行业 / 概念 / 地域板块 |
| `--period` | `今日` / `3日` / `5日` / `10日` | 资金流统计周期（仅实时查询） |
| `--top` | 数字 | overview / fund-flow 排行榜条数 |
| `--gainers-only` | 开关 | overview：全部上涨板块；detail：仅上涨个股 |
| `--hot` | 开关 | detail：涨幅前列 + 资金活跃双视图 |
| `--no-flow` | 开关 | 跳过主力流入/流出（更快） |
| `--workers` | 数字 | 历史查询并发数（默认 8） |
| `--limit` | 数字 | detail 命令显示条数 |
| `--sort` | `change` / `amount` / `volume` / `turnover` / `flow` | 成份股排序 |

## 回复格式

将脚本输出的 Markdown 表格整理后呈现给用户，并补充简短解读：

1. **概览**：点明最强/最弱板块、上涨家数统计、资金集中方向
2. **板块详情**：突出涨跌幅前列、成交额靠前、资金明显流入/流出的个股
3. **免责声明**：数据来自公开市场接口，存在延迟；非投资建议

示例结构：

```markdown
# A股板块速览（2026-06-26）

**统计**：共 496 个板块，上涨 33 | 下跌 463 | 平盘 0

## 涨幅前 10
| 板块 | 涨跌幅 |
| 橡胶助剂 | +5.41% |
...

## 有机硅 成份股（2026-06-26）
### 涨幅前列 / 资金活跃
| 代码 | 名称 | 涨跌幅 | 成交额 |
...

> 数据来源于东方财富，仅供参考。
```

## 常见问题

| 现象 | 处理 |
| --- | --- |
| `ModuleNotFoundError: akshare` | 运行 `pip install akshare pandas` |
| 非交易日 / 盘前数据为空 | 说明当日无交易或数据未更新，可改查 `--period 5日` 或换日期 |
| 历史查询很慢 | 正常现象；加 `--no-flow` 跳过资金流、降低 `--limit` |
| 板块名找不到 | 先 `list --type concept` 查准确名称，或用更短关键词模糊匹配 |
| 接口报错 | akshare 接口可能变更；重试或查阅 [akshare 文档](https://akshare.akfamily.xyz/) |

## 命令速查

```bash
# 行业板块今日概览
python ~/.cursor/skills/a-share-sector/scripts/query.py overview

# 6月26日哪些行业板块涨了（全部上涨列表）
python ~/.cursor/skills/a-share-sector/scripts/query.py overview --date 2026-06-26 --gainers-only

# 6月26日有机硅板块：涨得好 + 资金活跃个股
python ~/.cursor/skills/a-share-sector/scripts/query.py detail 有机硅 --date 2026-06-26 --hot --limit 5

# 概念板块资金流（历史）
python ~/.cursor/skills/a-share-sector/scripts/query.py fund-flow --date 2026-06-26 --type concept
```
