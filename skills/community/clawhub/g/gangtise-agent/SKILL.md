---
name: gangtise-agent
description: >
  通过 Gangtise Agent OpenAPI 统一拉取 Markdown 投研文本，面向「快速可读、少跳转」的研究与问答场景。
  各 Agent 能力概览：one-pager（公司一页通，单票核心要素与结论浓缩）；
  investment-logic（投资逻辑，主线叙事与关键假设）；
  peer-comparison（同业对比，竞争格局与可比公司差异）；
  earnings-review（绩点评，财报期业绩解读；需 getId 后轮询 getContent，最长约 600s）；
  viewpoint-debate（观点 PK，对给定观点的正反辨析与论据组织；同样异步轮询）；
  theme-tracking（主题跟踪，晨报/晚报式产业链与主题脉络）；
  research-outline（调研提纲，公司调研问题与访谈框架）；
  hot-topic-list（热点话题报告列表，按日期与报告类型分页拉取结构化热点，输出为多级 Markdown；核心标的为表格）；
  security-clue-list（投研线索列表，按证券/行业+时间范围提取研报、电话会议、公告、观点等结构化线索，输出为 Markdown 表格）。
  返回多为可直接引用的结论文本，适合纪要、速览、投研助理与 Agent 编排中的事实与观点补充。
version: 1.4.4
metadata:
  requires:
    env:
      - GTS_ACCESS_KEY
      - GTS_SECRET_KEY
    config:
      - path: scripts/.authorization
        required: false
        description: 用于配置ak/sk, 内容为{"accessKey":"<ak>", "secretAccessKey":"<sk>"}。与GTS_ACCESS_KEY和GTS_SECRET_KEY使用其一即可。如果同时存在，则以GTS_ACCESS_KEY和GTS_SECRET_KEY为准，建议环境变量配置不成功时使用文件配置。
  envVars:
    - name: GTS_ACCESS_KEY
      required: true
      description: 用于和GTS_SECRET_KEY一起获取临时 authorization
    - name: GTS_SECRET_KEY
      required: true
      description: 用于和GTS_ACCESS_KEY一起获取临时 authorization
---

# Agent 接口调用

## 概览

本技能通过 `scripts/agents.py` 调用通用 Agent 接口；`hot-topic-list` 与 `security-clue-list` 为独立脚本调用（参数差异较大）。

支持接口：

- `one-pager`：公司一页通
- `investment-logic`：投资逻辑
- `peer-comparison`：同业对比
- `earnings-review`：绩点评（自动串联 getId + 轮询 getContent，最长 600s）
- `viewpoint-debate`：观点 PK（自动串联 getId + 轮询 getContent，最长 600s）
- `theme-tracking`：主题跟踪（晨报/晚报）
- `research-outline`：公司调研提纲
- `hot-topic-list`：热点话题报告（早报/午报/盘中快报/晚报等，分页与多维筛选，结构化话题与可选标的/精读）
- `security-clue-list`：投研线索列表（按证券/行业查询，支持时间与来源筛选，分页最大 500）

授权方式与其他 gangtise 技能一致：在 `scripts/.authorization` 中配置 `long-term-token`，或配置 `accessKey` 与 `secretAccessKey`。

## 统一脚本

`scripts/agents.py`

`scripts/hot_topic.py`（仅 `hot-topic-list`）

`scripts/security_clue.py`（仅 `security-clue-list`）

## 参数说明

### `scripts/agents.py`

| 参数 | 必填 | 说明 |
|------|------|------|
| `-a` / `--agent-type` | 是 | 接口类型，见上方枚举。`earnings-review` 与 `viewpoint-debate` 会自动串联 getId + 轮询 getContent（最长 600s）。 |
| `-s` / `--security-code` | 条件必填 | 证券代码（如 `600519.SH`）。用于 `one-pager`、`investment-logic`、`peer-comparison`、`research-outline`、`earnings-review`。 |
| `-p` / `--period` | 条件必填 | 报告期（如 `2026q3`）。仅用于 `earnings-review`。 |
| `-d` / `--data-id` | 否 | 保留参数，当前无对外场景。 |
| `--viewpoint` | 条件必填 | 观点文本（最长 1000 字）。仅用于 `viewpoint-debate`。 |
| `-t` / `--theme-id` | 条件必填 | 主题 ID 或中文主题名（会按映射自动转为 ID）。仅用于 `theme-tracking`。 |
| `--date` | 条件必填 | 查询日期（`yyyy-MM-dd`）。仅用于 `theme-tracking`。 |
| `--type` | 条件必填 | 资讯类型（`morning`/`night`，支持逗号分隔多选）。仅用于 `theme-tracking`。 |

### `scripts/hot_topic.py`
| 参数 | 必填 | 说明 |
|------|------|------|
| `--page-from` | 否 | 分页起始偏移，默认 `0`。 |
| `--page-size` | 否 | 分页条数，默认 `500`，最大 `500`。 |
| `-sd` / `--start-date` | 否 | 开始日期，支持 `yyyy-MM-dd`。 |
| `-ed` / `--end-date` | 否 | 结束日期，支持 `yyyy-MM-dd`。 |
| `--hot-category` | 否 | 热点类型，逗号分隔：`morning`、`noon`、`afternoon`、`evening`。 |
| `--with-securities` | 否 | 是否包含相关证券。 |
| `--with-close-reading` | 否 | 是否包含精读。 |

### `scripts/security_clue.py`

| 参数 | 必填 | 说明 |
|------|------|------|
| `--page-from` | 否 | 分页起始偏移，默认 `0`。 |
| `--page-size` | 否 | 分页条数，默认 `500`，最大 `500`。 |
| `-st` / `--start-time` | 否 | 开始时间，支持 `yyyy-MM-dd` 或 `yyyy-MM-dd HH:mm:ss`。 |
| `-et` / `--end-time` | 否 | 结束时间，支持 `yyyy-MM-dd` 或 `yyyy-MM-dd HH:mm:ss`。 |
| `-q` / `--query-mode` | 是 | 查询方式：`bySecurity`（按证券）或 `byIndustry`（按行业）。 |
| `-g` / `--gts-code-list` | 是 | 证券/行业代码列表，逗号分隔；也可传 `all`。例如 `000001.SZ,000063.SH` 或 `888888.CI,999999.CI`。 |
| `--source` | 否 | 来源多选，逗号分隔：`researchReport`、`conference`、`announcement`、`view`。 |
| `-o` / `--output` | 否 | 结果保存路径。 |

## 示例

```bash
python3 scripts/agents.py -a one-pager -s 600519.SH
```

```bash
python3 scripts/agents.py -a investment-logic -s 600519.SH
```

```bash
python3 scripts/agents.py -a peer-comparison -s 600519.SH
```

```bash
python3 scripts/agents.py -a earnings-review -s 600519.SH -p 2025q3
```

```bash
python3 scripts/agents.py -a viewpoint-debate --viewpoint "飞天茅台的批价低点是1500元"
```

```bash
python3 scripts/agents.py -a theme-tracking -t 23600839952306231 --date 2026-03-01 --type morning,night
```

```bash
python3 scripts/agents.py -a theme-tracking -t 核电 --date 2026-04-01 --type morning,night
```

```bash
python3 scripts/agents.py -a research-outline -s 600519.SH
```

```bash
python3 scripts/hot_topic.py --page-from 0 --page-size 5 -sd 2026-03-22 -ed 2026-03-27 --hot-category morning,noon,afternoon --with-securities --with-close-reading
```

```bash
python3 scripts/security_clue.py --page-from 0 --page-size 10 -q bySecurity -g 000001.SZ,600519.SH
```

```bash
python3 scripts/security_clue.py --page-from 0 --page-size 10 -st "2026-03-01 00:00:00" -et "2026-03-23 23:59:59" -q byIndustry -g 888888.CI,999999.CI --source conference,view
```
