---
name: 1688-item-batch-opt-apply
displayName: 1688商品批量优化应用
displayDescription: 批量解析商品/素材优化任务，逐任务委托执行技能处理，结果展示与Excel导出，一键按item_id粒度应用到商品。
description: |
  1688商品批量优化应用
  用户需要对一批商品或素材进行批量优化并应用到商品时使用本技能；上游技能（商品诊断一键优化、店铺体检行动项）交接出批量任务清单时同样进入本技能；
  本技能是批量编排层：任务解析与确认（任意输入由主 Agent 结构化后统一入台账，当前主路径 ask_user 表单确认）、逐任务委托执行技能（1688-item-image-agent / 1688-item-title-optimizer 等）、逐任务落账（台账为唯一数据源）、执行结果展示与 Excel 产物导出（非交互式 present_files）、以及按 item_id 粒度的批量应用确认（当前逐任务单卡，batch-apply 单卡上线后升级）；
  本技能不直接生图、不直接写商品：生图与写入分别由执行技能与 MCP App 卡片组件完成；
  触发词：批量优化、批量处理、批量修图、批量换背景、批量白底图、批量生成主图、批量标题优化、把这些商品都优化一下、全部应用、批量应用到商品、一键应用到商品、批量融合、多图融合、图片合成、任务确认
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins:
        - python
  interactions:
    - name: confirm_batch_tasks
      type: ask_user_form
      description: "任务解析后当前主路径：ask_user（mode=form）多选题分页确认要执行的任务；batch-task-confirm 卡片组件上线后升级为单卡多选（见 references/interaction-specs.md）"
      required_data:
        tool: "ask_user"
        mode: "form"
    - name: batch_task_confirm_card
      type: mcp_app
      description: "升级路径（组件上线后启用）：Bash 直接执行 accio-mcp-cli call 弹 batch-task-confirm 单卡，多选/全选/反选后回传执行清单"
      required_data:
        tool: "offer_select_card"
        route: "batch-task-confirm"
    - name: batch_result_card
      type: mcp_app
      description: "升级路径（组件上线后启用）：弹出 batch-result-view 结果展示卡（进度+逐任务结果+应用入口）；当前用 Markdown 表格 + Excel 产物"
      required_data:
        tool: "offer_select_card"
        route: "batch-result-view"
    - name: batch_apply_card
      type: mcp_app
      description: "升级路径（组件上线后启用）：batch-apply 单卡一次勾选写入；当前逐任务弹执行技能自己的单条目应用卡"
      required_data:
        tool: "offer_select_card"
        route: "batch-apply"
---

# 1688-item-batch-opt-apply — 1688商品批量优化应用

## 技能定位（最高优先级）

本技能是**批量编排层**，覆盖钉钉需求《批量优化和应用技术拆解》的三段链路：
**任务解析及确认 → 执行结果展示 → 应用到商品**。

- **禁止旁路生图与写入**：不得绕开执行技能直接拼装生图指令，不得用任何非卡片通道写商品。
  生图由执行技能（按其 SKILL.md 规范）完成；当前写入商品使用执行技能的逐任务应用卡，
  批量应用卡提供并上线后改用 `batch-apply`。本技能 CLI 与主 Agent 均不直接写商品。
- **台账是唯一数据源**：所有任务、执行结果、应用回执都落
  `1688-item-batch-opt-apply/tasks.json`（当前工作目录下与本技能同名的目录内，
  与其他技能的产物目录隔离）；未落账的结果不会出现在展示与导出中。
  **每处理一个任务必须落账一次**，不做内存累积。
- **等待边界**：MCP App 卡片不阻塞。弹卡命令必须是本轮最后一个工具调用，调用后只输出
  一句不断言「已弹出」的引导语并立即结束本轮；退出码 0 不代表卡片已显示。用户提交后
  的回执作为**新的用户消息**到达，只从该消息读取选择/回执，不编造、不猜测。取消、
  空回执或组件失败不得被解释为已确认/已应用。
- **内部参数禁止复述**：卡片回传中的图片 URL、`applyParams`、`store_ref` 等内部字段仅作
  透传参数，禁止在面向用户的回复、进度、总结或错误说明中复述或展示。
- 本技能正式随 `1688-seller-assistant` 插件分发；读取插件内技能时携带对应 `plugin_id`。
  单独安装测试时按宿主提供的技能来源读取。复用宿主 AW 登录态，无自有 AK/Token 配置。

## 技能概述

用户提出「批量优化这些商品」「把这批素材都处理成白底图」「诊断结果全部应用」等批量诉求时，
本技能把任务结构化进台账、ask_user 表单确认、分批并行委托执行技能（每批 ≤5 任务）、
实时展示进度并导出
Excel 产物，用户看过完整方案并要求应用后才进入应用环节（当前逐任务单卡确认，
batch-apply 单卡组件上线后升级为一次勾选批量写入）。

### 阶段与等待边界

| 阶段 | 完成条件与下一步 |
|---|---|
| 任务确认（规则3） | 用户勾选要生成方案的任务；仅授权生成，不代表确认写入商品。 |
| 方案生成与展示（规则4、5） | 生成、落账、导出并展示完整方案；告知尚未应用，等待用户点击「应用」或明确要求应用。 |
| CPV 核对（规则6） | 收到应用意图后查询并核对；无须澄清则继续应用，需要澄清则暂停受影响商品的写入。 |
| 商品应用与回执（规则6） | 无须澄清的任务沿已授权通道应用；需要澄清的任务重新处理并展示终案，弹卡取得二次确认后应用。根据实际写入回执报告结果。 |

`status=success` 只表示方案生成成功，`apply_status=applied` 才表示商品应用成功。
方案生成进度 100% 或 Excel 已导出不代表商品已更新。用户未要求应用时，停在方案交付阶段
等待是正常流程，不自动推进 CPV 查询或写入；无须澄清的任务不额外增加二次确认，
现有应用组件自身的确认要求仍保留。无商品 ID 的素材任务交付产物后结束，不进入应用环节。

## 使用场景

- 用户口述或粘贴一批商品 + 优化要求（含上游商品诊断/店铺体检交接的结构化清单）
- 用户上传 Excel 任务文件或素材文件夹（主 Agent 读取结构化：商品ID+优化项、任意列语义、多列素材融合、每图独立处理等）
- 批量执行完成后要求导出结果 Excel / 下载文件
- 批量执行成功后要求「全部应用 / 一键应用到商品」

## 能力边界

- 只编排，不执行生图、不写商品（分别归执行技能与卡片组件）
- 优化项为封闭白名单（10 项，见规则2），表外诉求如实告知不支持并建议逐个走单任务技能
- 素材任务（folder 来源，无商品 ID）不进入应用环节
- 单批次建议 ≤40 个任务；超出时向用户建议分批

## CLI 命令

统一入口：`python3 "{baseDir}/cli.py" <command> [options]`，所有命令输出 JSON：
`{"success": bool, "markdown": str, "data": {...}}`。

### CLI 路径解析（每次执行 CLI 前必读）

`{baseDir}` 为本 Skill 的根目录（`cli.py` 所在目录），按以下规则解析：

1. 优先使用宿主 AccioWork 加载本 Skill 时提供的 `{baseDir}` 绝对路径。
   单独安装测试时同样使用宿主给出的实际 Skill 目录，不固定为账户级或 Agent 级目录。
2. 插件分发场景下，若 `{baseDir}` 未解析，可使用宿主提供的
   `PHOENIX_PLUGIN_ROOT_1688_SELLER_ASSISTANT` 拼接 `skills/1688-item-batch-opt-apply` 兜底。
   执行前确认该目录存在 `cli.py`，读取的 SKILL.md 与执行的 CLI 须来自同一份安装；
   路径仍不确定时检查宿主提供的技能路径，不猜测其他账户或 Agent 的目录。
3. 执行时把 `{baseDir}` 解析成完整绝对路径，并始终给整个脚本路径加引号；路径含空格或
   中文时也必须作为一个参数传入。

### Windows 执行约定

- Bash 是宿主工具名，不代表 Windows 上运行 bash；Windows 默认使用 PowerShell。多行 bash
  示例先合并成单行，不照搬 `\` 续行、`export` 或 `VAR=value command`。
- 优先使用 AccioWork 自带 `python3`；确认 `python` 可用后才替换命令名，不安装系统 Python。
- 普通文本参数用 PowerShell 字面量单引号包裹，文本中的单引号写成两个单引号。
- MCP App 卡片在 Windows 使用 `--json-file "<绝对路径>"`：先把卡片参数 JSON 写入系统临时
  目录唯一命名的 UTF-8 文件，再单独、直接执行 `accio-mcp-cli call ... --json-file "<绝对路径>"`。

### 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `parse_tasks` | 解析主 Agent 已结构化的任务进台账并出确认参数（可选 `--store_name` 记店铺名入台账，用于产物文件名前缀） | `cli.py parse_tasks --tasks '[...]' --store_name "<店铺展示名>"` |
| `query_offer_prop` | 按模型匹配词查询实际属性（每次 ≤20 商品） | `cli.py query_offer_prop --items_file "<JSON文件>"` |
| `save_result` | 单任务执行/应用结果落账（每任务必调） | `cli.py save_result --task_id T001 --status success --result_summary "..."` |
| `build_result_card` | 汇总台账生成结果展示参数（Markdown 进度/升级卡） | `cli.py build_result_card` |
| `export_results` | 导出 Excel 产物（openpyxl 缺失时 csv 兜底） | `cli.py export_results` |
| `build_apply_card` | 合并单条目应用参数生成批量应用卡（升级路径） | `cli.py build_apply_card --items '[...]'` |

> 详细参数、返回结构与展示规范见 `capabilities/<命令名>.md`；任务条目字段、op 映射、
> 状态机与主循环口径见 [references/task-contract.md](./references/task-contract.md)；
> 当前主路径（ask_user 表单 / Markdown / 逐任务单卡）与升级路径三卡契约见
> [references/interaction-specs.md](./references/interaction-specs.md)。

## ⚠️ 重要：技能使用规范

### 规则1：入口分支判定（必须最先执行）

**任何输入（口述、上游交接、Excel/任意文件、素材文件夹）都由主 Agent 自行读取理解
后结构化为标准任务数组**，再统一调用 `parse_tasks --tasks '<JSON数组>'`；脚本不解析
任何文件，列语义/文件配对猜测交给模型。任务数组两类条目：

- **商品任务**：`{"item_id":"<纯数字>","op":"<白名单项>","requirements":"<要求>","item_title":"<标题>"}`，可选 `input_images` 作参考图。
- **素材任务**：无 `item_id`，必填 `input_images`（单值或数组），可选 `source_file`
  标注源文件（如「model 列模特图 × scene 列场景图融合，每行一个任务」：主 Agent 读
  Excel 后每行产出 `{"op":"多图合成","input_images":[模特图,场景图],"requirements":...}`；
  素材文件夹场景列目录后每图产出 `{"op":"img_opt","input_images":[<图>],"source_file":<图>}`）。

上游技能交接的结构化 JSON（商品诊断 ONE_CLICK_OPTIMIZE、店铺体检行动项：
`products:[{offerId, title, optimizationPoints:[{opKey, label}]}]`）同样由主 Agent 转换
为上述标准数组（opKey→op 按 task-contract §2 映射，未映射项如实报告并询问用户）。

**店铺名传参**：宿主/上游侧（如 phoenix-pc 多店铺策略）给到当前操作店铺展示名时，
调用 parse_tasks 一并传 `--store_name "<店铺展示名>"`（仅用于产物文件名前缀，
避免多店铺同会话运行时产物文件名重叠；不参与鉴权）；取不到就不传，产物命名
不带店铺前缀（与旧版兼容）。

解析成功的 `data.warnings` 必须向用户展示；`new_count=0` 且有跳过/告警时如实说明，
不静默；随后进入规则3 任务确认（当前主路径 ask_user 表单，`data.confirm_card`
暂存备升级路径用）；不跳过确认直接执行。

### 规则2：优化项白名单与执行技能委托

op 为封闭白名单（解析层已拦截表外项），主 Agent 按下表把每个任务委托给对应执行技能，
**委托前必须读该执行技能的 SKILL.md** 并按其命令规范执行：

| op | 标签 | 执行技能 |
|---|---|---|
| `title_opt` | 标题优化 | 1688-item-title-optimizer |
| `main_img_opt` / `img_opt` / `bg_change` / `carousel_opt` / `detail_img_opt` / `full_img_set` / `full_listing_set` / `white_img_opt` | 图片类 8 项 | 1688-item-image-agent |
| `multi_img_merge` | 多图合成（素材融合） | 1688-item-image-agent（`multi_img_opt`；`--img_urls` 按任务 `input_images` 顺序，`--prompt` 按「图1、图2…」指代改写 requirements，图号=传入顺序） |

委托要点（完整口径见 task-contract §2）：商品 ID 原样传递不重选；执行技能内部交互
（如换背景先弹背景卡）按其自身规范执行。应用时机统一由本技能规则6 控制：先展示完整
优化结果，用户应用后查询 CPV，再由主 Agent 判断是否需要澄清。当前使用执行技能的
逐任务应用卡；批量应用卡提供并上线后，才将逐任务确认改为 batch-apply 单卡确认。
应用参数使用本轮最终方案；澄清后重新处理的任务须更新参数，再弹卡供用户二次确认。

标题任务按方案分别判断：CLI 报错或新标题缺失、为空、仅含空白时，该方案视为失败。
一个方案成功时保留并展示该方案，任务按生成成功落账，在 result_summary 中说明另一方案
未生成成功，不因单个方案失败把整条任务记为 failed；两个方案均失败才记录生成失败。
只有一个可用方案时仍须等待用户应用意图，再按规则6 核对 CPV，不自动应用。

### 规则3：任务确认（当前主路径：ask_user form；升级：batch-task-confirm 卡）

`parse_tasks` 成功并展示 `data.warnings` 后，确认环节按以下顺序选择通道。
确认内容须明确为「生成优化方案」，不能把本次任务确认当作后续商品写入授权：

**当前主路径（batch-task-confirm 组件未上线，勿弹 offer_select_card——未知 route 会被
组件按默认视图渲染成商品选择卡）**：宿主 `ask_user` 工具（`mode=form`）多选题分页确认：

- 每题 options 2-8 个（一题最多列 8 个任务，选项 label 用简短标识如「T001 主图优化·保温杯」），
  题目数 1-4；单轮 ask_user 最多确认 32 个任务，超出分批确认。
- question 限 500 字符：任务明细先在助手正文里用 Markdown 表格列清（taskId/商品/优化项/要求），
  ask_user 只做勾选确认，不在 question 里重复长清单。
- 回执落账**合并为一次执行**：单条 bash 串联逐任务 `save_result`（每任务仍是独立一次
  CLI 调用；已选 `--status confirmed`，未选 `--status skipped`），再进入规则4；取消/空选：
  停止执行，不把 parsed 任务默认执行。示例（`;` 分隔，不用 `&&`，单条失败不断链）：

  ```bash
  python3 "{baseDir}/cli.py" save_result --task_id T001 --status confirmed ; python3 "{baseDir}/cli.py" save_result --task_id T002 --status confirmed ; python3 "{baseDir}/cli.py" save_result --task_id T003 --status skipped
  ```

  任务多时每 ~10 个任务一条 bash 串联。**禁止**并行发起多条写台账的 bash 命令
  （台账是读改写文件，并行写会互相覆盖）。

**升级路径（1688GUI batch-task-confirm 组件上线且放量后）**：Bash 直接执行

```bash
accio-mcp-cli call --server accio offer_select_card --json '<parse_tasks.data.confirm_card 原样>'
```

不加 `--raw`、不接管道、不包在 Python 或 cli.py 里；弹卡后立即结束本轮；回执含勾选与
跳过的 taskId 清单，同样合并进单条 bash 串联落账后进入规则4。通道可用性以宿主/端侧
放量公告为准，未确认放量前一律走主路径。

### 规则4：分批并行执行主循环（每批 ≤5 任务）

确认清单按 **每批 ≤5 个任务** 分批执行（批次间串行；执行技能内部并发由其自身口径控制）。
`full_img_set` / `full_listing_set`（计划含 chain/后处理条目）建议单独成批或放批尾；
`title_opt` 文本类任务可混批。每批固定三个阶段：

**阶段一：启动 + 规划（一次迭代）**

同轮发起本批每任务一条 bash tool call，单条内串联「标运行 + 委托规划」：

```bash
python3 "{baseDir}/cli.py" save_result --task_id T001 --status running ; python3 "<image-agent cli.py 路径>" img_optimize --img_url '<图>' --user_requirements '<要求>'
```

各任务返回 `data.calls` 计划后，记录归属映射（tool_call_id → task_id → call_index）。
规划命令由各执行技能 SKILL.md 定义（委托前仍必须先读其 SKILL.md）。

**阶段二：生图（全局窗口调度，按轮推进）**

把本批所有任务的 calls 合并为一个**全局队列**，跨任务统一调度：

- 从队首取**连续独立条目**，全局在途 `image_generate` / `image_edit` 合计 **≤5 并行**发起；
- 遇任一任务的 chain/deliver 条目即截断（不跨屏障凑批）；该任务独立条目全部返回后，
  下一轮单独发起其 chain 条目；
- 本轮全部返回后才推进下一轮（同一轮消息内并行发起，不逐条串行调用）。

**阶段三：落账（一次迭代）**

单条 bash 串联逐任务 `save_result`（每任务独立一次调用）：

- 成功：`--status success --result_summary ... --result_images ...`（按 tool_call_id →
  task 归位取产物）；
- 失败：`--status failed --error <自然语言原因>`；
- 每批结束后用 `build_result_card` / Markdown 表格刷新一次进度（规则5），
  不逐任务刷屏。

**进度提醒（每批落账后立即向用户输出）**：以台账 `batch_stats` 为准，紧跟在本批
落账 bash 之后、启动下一批之前，用一条醒目单行向用户报告整体进度，格式：

```
## 📊 方案生成进度：已处理 40%（4/10）—— 生成成功 3 · 生成失败 1 · 剩余 6
```

- 百分比与计数一律取 `save_result` 返回的 `data.batch_stats`（total / by_status），
  不自行估算；skipped/cancelled 计入「已处理」；
- 同行附一句话状态（如批内新增失败原因摘要），不展开长表格；
- 最后一批后的进度行可并入结果总汇（规则5），不必重复输出。

**归位铁律**：结果按 `tool_call_id → task_id → call_index` 记录归属；失败/跳过条目保留
原下标，不按返回先后、URL 或压缩成功列表匹配；单任务失败不阻断批内其他任务，
记录原因后继续。**禁止**并行发起多条含 `save_result` 的 bash 命令（台账读改写互斥）。

用户中途要求停止：已启动的调用等待返回后按实际结果落账；未启动任务落
`--status cancelled`，已产出如实交付。

### 规则5：执行结果展示与 Excel 导出（当前主路径：Markdown + Excel；升级：batch-result-view 卡）

- **当前主路径（batch-result-view 组件未上线）**：进度与结果用助手正文 Markdown 表格
  展示（无长度限制：taskId/商品/优化项/生成状态/应用状态/结果摘要/失败原因；建议每完成若干任务或
  阶段结束时更新一次，不逐任务刷屏）；**每批落账后先输出一条醒目进度行**
  （「方案生成进度：已处理 xx%（xx/xx）—— 生成成功 x · 生成失败 x · 剩余 x」，口径见规则4 阶段三）；
  `build_result_card` 返回的 `data.card` 先落账备用，不弹卡。
- **完整方案与等待应用**：标题展示原标题和完整拟应用标题，图片展示生成的图片，其他优化项
  展示对应内容；进度、结果摘要和 Excel 下载入口不能代替完整方案展示。
  对首次生成成功、尚未应用的商品明确提示「优化方案已生成，尚未应用到商品，请确认是否应用」。
  展示后结束本轮，等待用户点击「应用」或明确要求应用，再进入规则6；
  应用状态按台账实际值展示，不把「生成成功」写成「更新成功」或「应用成功」。
- **升级路径（组件上线且放量后）**：把 `data.card` 原样弹 `offer_select_card`
  （route=`batch-result-view`）刷新进度；弹卡仍是本轮最后一个工具调用。
- Excel 导出（钉钉文档口径：非交互式，在产物中展示）：**批次执行结束（全部批次
  落账完成）后自动执行** `export_results`，成功后按 `data.file_path` 与
  `data.package_path`（zip 包，存在时）调用宿主 `present_files` 展示产物文件
  （表格 + 全部产物图打包，用户可一键下载）；导出失败不阻断收尾，如实告知后
  按用户要求重试；不把文件路径再贴长链接给用户。
- **产物路径与防覆盖**：全部产物（表格/zip/台账）均落在会话工作区
  `1688-item-batch-opt-apply/` 目录内；台账带 `store_name`（parse_tasks
  `--store_name` 传入）时，导出与归档文件名带店铺前缀
  （`批量任务结果_<店铺>_<批次ID>.xlsx` / `tasks_<店铺>_<旧批次ID>.json`），
  多店铺同会话运行不撞名；同批次重复导出或撞名时文件名自动加序号
  （`_2`、`_3`…），多批次/多店铺同会话运行不会互相覆盖，不要手动改名或复用旧产物文件名。

### 规则6：应用到商品（当前主路径：逐任务单卡；升级：batch-apply 单卡）

先展示完整优化结果，用户点击「应用」或明确要求应用后，再查询商品当前 CPV。
首次确认优化任务不触发此查询。查询结果只交给主 Agent 使用，不落账。

1. **查询**：主 Agent 根据用户目标、优化内容生成 `propertyNames` 匹配词数组，例如主图
   使用 `["主图","轮播图","首图","商品图","图片"]`。工具内部据此生成正则，缩小返回范围。
   同商品合并匹配词，唯一商品每批最多 20 个，调用
   `query_offer_prop --items_file "<JSON数组文件>"`，详见 [query_offer_prop](capabilities/query_offer_prop.md)。
2. **主 Agent 对比判断：先 key，后 value**。直接读取真实 CPV，先根据 `name/label`
   核对模型生成的 key 是否存在、是否能明确对应到目标属性。key 未找到或对应关系有歧义时，
   不能放行，也不能仅因某个属性的候选包含目标 value 就擅自替换 key；需由主 Agent 澄清。
   查询经过匹配词过滤，未返回某个 key 不等于商品一定不存在该属性，必要时补充相关词查询。
   key 明确后，再按该属性的 inputType 判断用户输入的 value：SINGLE_SELECT 检查单个值
   是否在候选内，MULTI_SELECT 检查所选值是否都在候选内，TEXT_INPUT 不校验 value，
   但仍须完成 key 核对。`values` 是当前值，`candidates` 是候选值，新旧值不同本身是正常修改。
   例如“颜料改成磨砂”，返回中只有“材质”且其候选包含“磨砂”，仍需澄清是否修改“材质”，
   不能因为“磨砂”属于候选就直接放行。
3. **分流**：无须澄清，进入第6步，沿已授权的应用通道更新商品并展示实际应用结果，
   不额外执行第4、5步的澄清与二次确认；
   需要澄清，先暂停受影响商品的更新，由主 Agent 结合原始要求、优化方案及 CPV
   自行生成澄清内容。查询失败或返回不足以判断时，不能当作无问题直接更新。
4. **澄清分支的重新处理**：用户回答后，主 Agent 根据澄清内容重新处理受影响的优化内容，
   需要重新生成标题或图片时调用对应执行技能，并更新完整最终方案及应用参数。
   主 Agent 对照真实 CPV 判断处理后的方案是否可以应用；仍有问题则继续澄清，暂不更新商品。
5. **澄清分支的弹卡二次确认**：第4步处理完成后先展示完整最终方案，再弹出执行技能对应的确认应用卡片，
   让用户点击「确认应用」。收到第二次确认后才按新方案更新商品并展示结果。
   澄清回答本身不等于最终确认，不复用澄清前的旧方案或旧卡片参数。
6. **应用与回执**：更新仍走执行技能既有应用通道，使用最终确认的方案。
   当前主路径是逐任务应用卡；batch-apply 组件上线后才使用 build_apply_card。
   宿主第一次「应用」必须先回传应用意图，查询和判断后再写入；当前组件自身的确认约束仍保留。
   实际写入回执到达后，用 save_result 记录 applied/failed/cancelled/unknown；
   CPV 查询结果、对比判断和澄清过程不写入台账。unknown 按“已提交应用，稍后到商家后台核对”转述。

### 规则7：展示与转述规范

- 面向用户展示任务数、商品标题、优化项、进度、结果摘要、应用状态，以及核对时必要的属性名、值、差异与最终方案；不展示
  task_id 之外的内部字段、图片 URL、`applyParams`、`store_ref`。
- 积分/耗时预期提醒沿用各执行技能 SKILL.md 的口径（如 image-agent 多图 ≥5 张派发前提醒）。
- 批量场景不要逐任务输出长篇过程叙述；用进度摘要 + 最终结果卡收敛。
- 降级链路发生时如实告知，不得静默假装卡片已展示。

## 异常处理

- CLI 返回 `success:false`：先按实际返回区分参数错误、平台业务拒绝和结果未知。
  参数错误可修正后重试；商品写入按下述回执规则处理，不因 `success:false` 自动重复提交。
- 台账缺失/为空：先 `parse_tasks`；用户在未确认/未落账状态下要求应用：如实说明先完成执行。
- 卡片加载失败（命令报错/超时/退出码非 0）：按「卡片加载失败」如实告知，不自动重试；
  用户明确要求重弹时视为新指令重新走 build + 弹卡。
- 生成阶段的执行技能失败：落账 `status=failed` + 原因，继续批次；批次结束在结果汇总中统一呈现失败清单。
- **平台明确拒绝写入**：CPV 核对通过不代表平台一定允许修改。根据真实写入回执，
  用 `save_result --apply_status failed --apply_detail "<平台返回的失败原因>"` 记录；
  保留已有 `status=success` 和生成方案，不把应用失败改记为生成失败。
- **官方活动锁定**：写入回执明确返回「商品参加1688官方活动，部分核心信息禁止修改」等限制时，
  按上述规则记录应用失败，并告知「方案已生成，但受活动限制，未能应用」。保留方案，
  引导用户到商家后台查看活动状态，限制解除后再由用户发起应用；限制未解除时不自动重复提交。
  其他已获应用授权且不受影响的商品继续处理，逐商品展示实际结果。
  仅提供工具返回的官方链接或已确认适用于该问题的官方链接，不固定附带未经核实的活动短链接。
- 写入请求已提交但应用回执缺失、超时或无法确认是否生效：置 `apply_status=unknown`，
  提示用户到商家后台核对，不判定成功或失败，也不自动重试写入。

## 环境与依赖

- Python 3.8+；Excel 导出优先使用 openpyxl（缺失时自动降级 csv，utf-8-sig 编码，
  Excel 打开不乱码），不因缺依赖阻断主流程。
- 本技能 `.env` 仅含平台占位符（SKILL_NAME/SKILL_VERSION/SKILL_CHANNEL），无 AK/Token；
  登录态复用宿主 AW 会话。

## 执行前检查清单

- [ ] 已按「CLI 路径解析」确定 `{baseDir}` 绝对路径，读取与执行来自同一份安装，plugin_id 与宿主提供的技能来源一致
- [ ] 任务已 `parse_tasks` 进台账，warnings 已展示，任务确认（当前主路径 ask_user 表单）已回执，逐任务 confirmed/skipped 已合并进单条 bash 串联落账
- [ ] 每个任务委托执行技能前已读其 SKILL.md；执行按规则4 分批并行（每批 ≤5 任务，全局在途生图 ≤5）；每批结束即串联 `save_result` 落账
- [ ] 写台账的 bash 从不并行发起（单条 bash 内串联）；生图结果按 tool_call_id → task_id → call_index 归位，未按返回先后/URL 匹配
- [ ] 每批落账后已向用户输出醒目的方案生成进度（已处理 xx%（xx/xx），取自 batch_stats）；未把生成成功当作应用成功
- [ ] 已展示完整优化方案和实际应用状态；首次应用前明确告知尚未应用，未将任务确认或 Excel 导出当作应用授权
- [ ] 弹卡（升级路径三卡与当前逐任务单卡）均为 Bash 直接执行 `accio-mcp-cli call`，且是本轮最后一个工具调用
- [ ] 进入应用环节时，已收到用户看过完整方案后的应用意图并定向查询 CPV；需要澄清的任务已澄清、重新处理并获得终案二次确认；CPV 信息仅用于当前上下文
- [ ] 卡片回执只从新用户消息读取；apply 回执已逐任务落账
- [ ] 面向用户的输出未复述图片 URL、applyParams、store_ref 等内部字段
- [ ] 批次执行结束后已自动 `export_results` 并 present_files（表格 + zip 产物包）；失败时已如实告知
- [ ] Excel 导出走 `present_files` 非交互式展示
- [ ] unknown 状态按「已提交待核对」口径转述
