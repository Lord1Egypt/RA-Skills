---
name: feishu_ingest
description: Poll Feishu groups for new messages, download message resources, read Feishu docs/wiki/sheets/bitables, compile message-source markdown, judge which chat segments are worth preserving, and ingest valuable materials into the Research KB through a prepare/apply workflow.
---

# feishu_ingest

## 职责

把飞书群作为可定时扫描资料源处理。`prepare` 拉取增量群消息、下载消息资源、读取飞书云文档、把普通群消息编译成可定位的 Markdown 源文件，并输出供 OpenClaw 分析的 `inputItems[]`。`apply` 校验 OpenClaw 生成的页面、归档源文件、写入 Gitea 知识库、更新 `catalog.json` / `index.md`，并返回 `sourceItems[]` 给后端持久化。当前“群文件”来自群消息历史里的 file/image 等 message resource；不单独爬取群文件目录，飞书文件夹消息记录为 `unsupported`。

不要伪造飞书内容。缺少凭据、机器人不在群、无权限读取消息/文件/文档时，返回 `need_authorization` 或明确错误。飞书文件夹和超大文件记录为 `unsupported`。

飞书内容往往是碎片化线索，入库前必须先判断它在知识库图谱里的位置。写 `pages.json` 前，OpenClaw 应私下做一次知识图谱规划：哪些文件/文档/消息片段值得成为实体页，哪些已有 `overview/`、`projects/`、`concepts/`、`resources/` 或其他页面需要补充新证据和跳转。不要把低价值聊天硬写成页面，也不要把稳定概念、具体资源或团队导航更新遗漏掉。

## 脚本结构

当前 `scripts/` 只保留真实入口和依赖：

- `run_task.py`：唯一命令入口，提供 `prepare` 和 `apply` 子命令。
- `feishu_reader.py`：prepare 主逻辑，拉消息、处理附件/云文档/消息片段、生成分析上下文。
- `kb_writer.py`：apply 主逻辑，校验 `sourceItemKeys`、归档源文件、写页面/catalog/index、生成 `sourceItems[]`。
- `feishu_platform.py`：飞书开放平台客户端，负责 token、消息历史、消息资源、Doc/Wiki/Sheet/Bitable 读取。
- `text_extractors.py`：本地文件文本预览，支持文本、CSV/JSON/YAML/代码、DOCX、PPTX、XLSX、PDF 可选解析、ZIP 清单。
- `gitea_api.py`：Gitea 内容读写客户端，支持 dry-run。
- `catalog.py`：catalog 合并、索引渲染、图关系归一。
- `task_io.py`：payload/result JSON 读写。
- `utils.py`：hash、slug、frontmatter 清理、关键词、路径安全等通用函数。

旧探索脚本已删除；飞书读取统一走 `feishu_platform.py`，知识库写入统一走 `kb_writer.py`。

## 必需配置

环境变量：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `GITEA_URL`
- `GITEA_BOT_TOKEN`
- `GITEA_BOT_USERNAME` 或 `GITEA_ORG`
- `TEAM_KB_REPO`

可选：

- `OPENCLAW_SHARED_DIR`：token 缓存、prepare 临时文件和中间上下文目录。

飞书应用需要机器人能力、机器人已进群、读取群消息历史权限、读取群消息资源权限。读取云文档还需要对应 Doc/Wiki/Sheet/Bitable 权限和文档授权。

## 输入配置

后端资料源会传入：

- `source.config.chatId` / `openChatId` / `open_chat_id`：飞书群 ID。
- `scanIntervalMinutes`：后端定时扫描间隔。
- `initialLookbackHours`：首次扫描回扫窗口，默认 168 小时。
- `maxMessages`：每轮最多拉取消息数，默认 200。
- `messageSegmentWindowMinutes`：把相邻群消息编译成一个消息源文件的时间窗口，默认 10 分钟。
- `maxMessagesPerSegment`：每个消息源文件最多包含的消息数，默认 12。
- `maxFileSizeMb`：单个群文件进入分析的最大体积，上限 100MB。
- `includeFiles` / `includeMessages` / `includeDocuments`：是否处理群文件、普通群消息、飞书云文档。
- `fetchRecentMessages=false`：只处理后端传入的 `source.items[]`，不主动拉群消息。
- `urls` / `docUrls` / `wikiUrls` / `tokens` / `documents` / `links`：额外飞书文档、Wiki、表格、多维表格 URL 或 token。
- `source.lastSnapshot.lastMessageCreateTime`：上一轮处理到的消息创建时间，prepare 用它做增量游标。

## Prepare

运行：

```bash
python3 scripts/run_task.py prepare --input <payload.json> --context-output <context.json>
```

prepare 输出：

- `inputItems[]`：OpenClaw 需要分析的候选资料。
- `sourceItems[]`：prepare 阶段已经确定为跳过、无权限、失败、暂不支持的资料项。
- `instructions.analysisTemplates`：每种资料类型的分析模板。
- `skipResult`：没有新候选资料时直接写给后端的成功结果；如果没有写入任何页面且 `sourceItems[]` 中存在 `need_authorization` 或 `fetch_failed`，后端会把任务标记为 `failed` 并保留 result/sourceItems 作为诊断。

`inputItems[]` 类型：

- `sourceKind=feishu_file`：群消息里的文件/图片等下载资源，`required=true`。后续按本地文件同样思路分析，并归档原始文件。
- `sourceKind=feishu_document`：飞书云文档/Wiki/Sheet/Bitable 编译出的 Markdown 源，`required=true`。
- `sourceKind=feishu_message_segment`：按时间窗口整理后的群消息片段，`required=false`。源文件包含发送时间、message_id、sender、消息原文和机器可读定位。

## OpenClaw 生成 pages.json

强制规则：

- 文件和云文档：每个 `required=true` 的 input item 必须出现在至少一个页面的 `sourceItemKeys` 中。
- 群消息：不要逐条入库。只在消息片段包含长期研究价值时写入 `notes/`。
- 高价值消息包括：项目决策、需求澄清、可复用解释、实验结果、会议结论、资源链接加上下文、后续行动项。
- 低价值消息包括：收到/好的/谢谢、纯排期、重复通知、无上下文链接、临时协调、表情或闲聊。
- 生成页面时必须保留 `sourceItemKeys`。不要写 `source_files/`，源文件归档由 apply 完成。
- 不写 `qa/` 页面。
- 根据证据生成/更新 `overview/`、`concepts/`、`resources/`、`projects/` 等相关页面时，要在正文里写 Markdown 链接，并维护 `relatedConcepts` / `relatedResources` / `relatedCodePages` / `relatedPages`。`relatedPages` 用于 overview、项目、论文、综述、会议、实验、技术文档、笔记等普通 Wiki 页面之间的关联。

## Apply

运行：

```bash
python3 scripts/run_task.py apply --input <payload.json> --context <context.json> --pages <pages.json>
```

apply 会：

1. 校验所有页面路径和 `sourceItemKeys`。
2. 确认所有 required 文件/云文档已被页面覆盖。
3. 把被使用的群文件归档到 `source_files/feishu/<sourceId>/files/`。
4. 把被使用的群消息源 Markdown 归档到 `source_files/feishu/<sourceId>/messages/`。
5. 把被使用的飞书云文档源 Markdown 归档到 `source_files/feishu/<sourceId>/documents/`。
6. 写入页面、`catalog.json`、`index.md`。
7. 返回 `sourceItems[]`，标记每个资料项为 `ingested`、`skipped`、`need_authorization`、`fetch_failed` 或 `unsupported`。

## 页面路由与模板

### `papers/` 论文/技术报告

适用：论文 PDF、arXiv、会议论文、技术报告。覆盖：摘要、研究问题、方法、数据/实验、主要结论、局限、可复用点、相关概念与资源。

### `surveys/` 综述/调研

适用：行业调研、文献综述、方案对比、landscape。覆盖：范围、分类框架、对比表、趋势、空白/争议、推荐阅读、相关概念与资源。优先做结构化比较。

### `projects/` 项目/需求/方案

适用：需求文档、项目计划、路线图、方案评审。覆盖：背景、目标、范围、里程碑、关键决策、风险、下一步、相关页面。

### `code/` 代码/仓库/接口

适用：代码文件、仓库说明、API 文档、SDK、脚本。覆盖：仓库/模块、架构、入口、关键 API、运行/部署、风险与 TODO、相关概念。

### `meetings/` 会议/讨论

适用：会议纪要、长讨论、同步会摘要。覆盖：背景、讨论要点、决策、行动项、开放问题、相关页面。不要逐字转写。

### `experiments/` 实验/评测

适用：实验记录、benchmark、ablation、结果表、失败复盘。覆盖：假设、设置、指标、结果、分析、复现信息、后续实验。

### `tech-notes/` 技术笔记/排障

适用：部署手册、配置说明、排障过程、命令记录。覆盖：问题、环境、步骤、配置、排错、参考、相关页面。

### `notes/` 群消息沉淀

适用：经过价值判断的普通群消息片段。覆盖：背景、要点、结论/价值、后续动作、消息定位。消息定位至少包含时间范围和 message_id。

### `concepts/` 概念页

适用：从资料中抽出的稳定概念、方法、术语。覆盖：定义、使用场景、相关方法、常见误区、相关资源。概念页要链接回支撑资料页。

### `resources/` 资源页

适用：工具、链接、数据集、附件、图片、暂不能深度解析但值得登记的资料。覆盖：资源是什么、内容摘要、使用方法、适用场景、限制、相关页面。

### `overview/` 总览/导航页

适用：飞书消息或文档显著改变团队级主题导航、项目资料地图、阶段性资料包、研究方向入口或跨资料综合时。覆盖：主题边界、相关实体页、关键概念/资源、当前状态、待补证据。没有明确导航或综合价值时不要硬建 overview。

## 输出结果

成功结果必须包含：

```json
{
  "success": true,
  "processedSources": ["source-item-key"],
  "createdPages": [],
  "updatedPages": [],
  "archivedFiles": [],
  "skippedSources": [],
  "errors": [],
  "commitId": "",
  "snapshot": { "lastMessageCreateTime": 0 },
  "sourceItems": []
}
```

`sourceItems[]` 每项尽量包含：`itemKey`、`sourceKind/kind`、`status`、`title`、`sha256`、`relativePath/originalPath`、`archivedPath`、`url`、`externalId`、`messageTime`、`size`、`lastError`、`metadata`。前端飞书资料源卡片中的资料项状态统计来自后端持久化后的 `source_items` 累计数据；最新游标/消息/候选数来自本轮 snapshot。

如果没有新增消息、文件或文档，prepare 可以直接写入成功的 skip result。若只有普通群消息且 OpenClaw 判断都不值得入库，apply 允许 `pages: []` 并更新快照，避免下轮重复处理。
