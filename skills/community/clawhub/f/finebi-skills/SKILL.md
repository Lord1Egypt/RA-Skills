---
name: "finebi-skills"
description: "FineBI 主技能入口。先识别用户目标，再路由到 dashboard-briefing、report-to-doc、alert-to-task、sync-to-bitable 等子技能。"
version: 0.2.33
author: zsmj1994
tags:
  - finebi
  - skill-router
  - business-intelligence
  - reporting
metadata:
  clawdbot:
    emoji: "📊"
    primaryEnv: "FINEBI_BASE_URL"
    install: "npm install -g finebi-cli"
    requires:
      bins: ["node", "finebi-cli"]
      env: ["FINEBI_BASE_URL", "FINE_ACCESS_TOKEN"]
runner: cli
entrypoint: finebi-cli
---

# FineBI 主技能

这个文件是 `finebi-skills` 包的主技能入口。它负责先识别用户目标，再路由到合适的子技能，而不是把所有场景的细节流程都堆在一个文件里。

## 运行前提

`finebi-skills` 依赖外部 CLI：

- 必须先安装 `finebi-cli`
- 必须能在终端里直接执行 `finebi-cli`
- 必须配置 FineBI 访问所需环境变量

推荐安装方式：

```bash
npm install -g finebi-cli
```

## 常见配置方式

有两种常见方式可以让 `finebi-skills` 读到 FineBI 配置：

1. 单独使用 `finebi-cli`

- 运行 `finebi-cli init`
- 配置会写入 `~/.finebi-cli/.env`
- 之后可以在任意目录使用 `finebi-cli`

2. 在 OpenClaw 等宿主工具中使用

- 用户可以直接把 `FINEBI_BASE_URL`、`FINE_ACCESS_TOKEN` 配置到宿主工具自己的 `.env`
- 如果宿主在启动 `finebi-cli` 时会自动带上这些环境变量，skill 就可以直接复用它们
- 这种情况下不一定需要单独运行 `finebi-cli init`

## 启动检查

在进入任何子技能流程之前，先做下面的检查：

1. 检查 `finebi-cli` 是否可执行。
2. 检查 `FINEBI_BASE_URL` 是否已配置。
3. 检查认证信息是否已配置，例如 `FINE_ACCESS_TOKEN`。

如果 `finebi-cli` 不可用：

- 不要继续执行后续 workflow
- 先明确提示用户安装 `finebi-cli`

如果环境变量缺失：

- 不要伪造连接结果
- 先提示用户完成 FineBI 连接配置

## 什么时候先用主技能

当用户要做下面这些事情时，先命中这个主技能：

- 查找并分析看板、组件和指标
- 生成日报、周报、月报或经营分析文档
- 监控阈值并转成任务或提醒
- 把 FineBI 数据同步到外部表格系统

## 子技能索引

| 子技能 | 目录 | 处理场景 |
| --- | --- | --- |
| `dashboard-briefing` | `skills/dashboard-briefing` | 看板摘要、群播报、定时简报 |
| `report-to-doc` | `skills/report-to-doc` | 看板导出、分析报告、文档沉淀 |
| `alert-to-task` | `skills/alert-to-task` | 阈值监控、异常检测、任务创建 |
| `sync-to-bitable` | `skills/sync-to-bitable` | 数据同步到飞书多维表格 |

## 路由规则

### 路由到 `dashboard-briefing`

当用户提到以下意图时优先路由：

- “给我生成日报/周报摘要”
- “把经营看板同步到群里”
- “做一个定时播报”
- “先发一条测试卡片看看”

### 路由到 `report-to-doc`

当用户提到以下意图时优先路由：

- “把这个看板整理成文档”
- “导出 PDF 后做分析报告”
- “给我一份经营分析稿”
- “把图表和结论沉淀成文档”

### 路由到 `alert-to-task`

当用户提到以下意图时优先路由：

- “低于阈值就告警”
- “异常时自动建任务”
- “监控库存、销量、回款”
- “命中条件后通知负责人”

### 路由到 `sync-to-bitable`

当用户提到以下意图时优先路由：

- “同步到飞书多维表格”
- “按主键增量更新”
- “覆盖整张表”
- “定时把数据灌到 bitable”

## 全局约束

- 先确认 `finebi-cli` 和 FineBI 环境可用，再执行业务流程。
- 先定位数据对象，再执行动作。数据对象可能是 `dashboard`、`dataset`、`subject`、`widget`。
- 看板问答、指标解释和组件取数场景，必须先按 `references/dashboard-question-answer-flow.md` 执行。
- 只要后续流程需要看板的id `dashboardId`，必须先按 `references/dashboard-id-resolution-flow.md` 判断来源并解析 id。
- 定位仪表板时，默认先从挂出目录或已发布入口查找，再从“我的分析”查找。
- 调用 `get-entry-tree` 读取目录树时，应优先使用 `-k <keyword>` 过滤，避免拉取过大的目录树响应。同时注意`get-entry-tree` 的响应结果中的`templateId`禁止作为 `dashboardId` 使用。
- `export-dashboard-excel` 获取仪表板中所有组件完整数据。
- 只有用户明确要求某个具体组件、图表或指标卡的数据时，才进入组件取数链路。
- 组件取数必须先用 `resolve-dashboard-widgets` 获取可取数组件候选，再调用 `get-widget-data`。
- 先拿到 FineBI 的真实输出，再做摘要、判断、告警、写文档或同步。
- 复核 FineBI Excel 导出内容时，必须用 `read_only=False` 打开工作簿检查真实单元格内容。
- 禁止伪造指标、趋势、负责人、任务状态、导出结果和同步结果。
- 禁止仅凭 read-only 模式下的 `max_row`、`max_column` 或首行预览判断 Excel “无数据”或“只有表头”。
- 禁止通过自写 JS、Python、浏览器自动化、抓包或猜 HTTP 接口等方式绕过 `finebi-cli` 查找 `dashboardId`、`widgetId` 或数据。
- 如果 CLI 链路无法定位目标，必须停止并澄清或报告“缺少 CLI 能力”，不要自建替代链路。
- 如果目标对象不唯一，必须先澄清，不能跳步。
- 如果子技能匹配已经明确，直接按子技能流程继续，不要在主技能里重复展开细节。

## 公共参考

- CLI 命令与契约：`references/cli-command-map.md`
- 看板问答取数链路：`references/dashboard-question-answer-flow.md`
- 仪表板 id 解析：`references/dashboard-id-resolution-flow.md`
- 仪表板组件取数：`references/dashboard-widget-data-flow.md`
- 数据集查找与预览：`references/dataset-search-and-preview-flow.md`
- 路由与拆分约定：`references/skill-routing.md`

## 无匹配时的降级策略

如果用户目标不能明确落到某一个子技能：

1. 先判断更像“看板消费”还是“数据集处理”。
2. 如果更像看板消费场景，优先走 `dashboard-briefing`。
3. 如果更像数据搬运或落库场景，优先走 `sync-to-bitable`。
4. 如果仍然不明确，只追问一个关键问题，不要一次追问多个问题。
