# 批量任务契约（task-contract）

本文是 SKILL.md 的规范补充：任务条目结构、op 白名单与执行技能映射、台账状态机、
主循环（分批并行委托执行，每批 ≤5 任务）与交接结构。SKILL.md 保持操作流程，
字段级口径以本文为准。

## 1. 任务条目（台账 & 确认卡）

| 字段 | 类型 | 说明 |
|---|---|---|
| `task_id` | str | 批次内唯一（T001 起），由 parse_tasks 分配，全程不改 |
| `item_id` | str | 商品 ID（纯数字）。素材任务（folder 来源）为空串 |
| `item_title` | str | 商品标题（解析来源提供则带，否则空） |
| `op` | str | 优化项键（见 §2 白名单） |
| `op_label` | str | 优化项中文标签 |
| `requirements` | str | 用户要求原文转述 |
| `input_images` | list | 输入图列表（https:// 或本地路径）。素材任务必填；商品任务可选（作参考图） |
| `source` | str | 固定 `context`：所有输入均由主 Agent 结构化后统一进入（无 excel/folder 通道） |
| `source_file` | str | 可选，主 Agent 从文件/文件夹读取时标注的源文件路径，便于追溯 |
| `status` | str | 执行状态（见 §3 状态机） |
| `apply_status` | str | 应用状态（见 §3 状态机） |
| `result_summary` | str | 执行结果一句话摘要 |
| `result_images` | list | 执行产物（https:// 链接或 media-output 本地路径） |
| `apply_detail` | str | 应用回执自然语言摘要 |
| `error` | str | 失败原因（自然语言，可对用户展示） |

## 2. op 白名单与执行技能映射

主 Agent 按下表把每个任务委托给对应执行技能（读该技能 SKILL.md 后按其规范执行）。
**映射是封闭集合**：不在表内的 op 不进入台账（parse_tasks 已在解析层拦截）。

| op | 标签 | 执行技能 | 委托要点 |
|---|---|---|---|
| `title_opt` | 标题优化 | 1688-item-title-optimizer | 传 item_id 与 requirements；结果为新标题文本 |
| `main_img_opt` | 主图优化 | 1688-item-image-agent | `img_optimize`（优化主图）；产物为图片 |
| `white_img_opt` | 白底图 | 1688-item-image-agent | `white_bg`；默认 800×800 |
| `img_opt` | 图片优化 | 1688-item-image-agent | `img_optimize`（通用增强/修图） |
| `bg_change` | 背景替换 | 1688-item-image-agent | `bg_change`；缺背景方案时按该技能规则先弹 background-select 卡 |
| `carousel_opt` | 副图轮播图 | 1688-item-image-agent | `gen_secondary_image`（默认 3 张，≤5） |
| `detail_img_opt` | 详情图 | 1688-item-image-agent | `gen_detail_image`（默认 6 张，≤8） |
| `full_img_set` | 一套主图 | 1688-item-image-agent | `full_main_image_set` |
| `full_listing_set` | 全套上架图 | 1688-item-image-agent | `full_listing_image_set`；先展示其 data.reminder |
| `multi_img_merge` | 多图合成 | 1688-item-image-agent | `multi_img_opt`；`--img_urls` 按任务 `input_images` 顺序传入，`--prompt` 把 requirements 改写为「图1、图2…」明示指代（图号=传入顺序，image-agent 契约）；无商品 ID 时 offerId 语义由该技能口径处理 |

**交接规则**：
- 商品 ID 缺失但带 `input_images` 的任务为**素材任务**（Excel 多列融合、文件夹每图
  独立或配对组合等，均由主 Agent 读取结构化后传入）；素材任务不进入应用环节，
  判重按 `(input_images 序列, op)`，带 `source_file` 时按 `(source_file, op)`。
- 委托时商品 ID 原样传递（不重选、不弹 select 卡：批量场景商品 ID 来自用户/台账，
  已是确定输入；执行技能商品 ID 认定口径已覆盖「上游交接产出中的商品 ID」）。
- 每个任务是一个独立委托：执行技能按其自身规范完成交互（如换背景先弹背景卡）、
  生成与应用前置（authorize_item / prepare_image_apply）。
- 应用时机由 SKILL.md 规则6 统一控制：当前使用执行技能的逐任务应用卡；
  批量应用卡提供并上线后，才改为 batch-apply 单卡确认。
  用户应用后先查询 CPV，由主 Agent 对比并处理澄清；澄清后重新处理、更新应用参数，
  再弹确认应用卡片供用户二次确认，不在生成优化结果时提前发起写入。
- `apply_to_item`（标题等非图片写入）：标题优化等文本类执行技能的写入环节，
  按该技能自身规范执行；其回执同样经 save_result 落账（apply_status）。

## 3. 台账状态机

CPV 查询结果不进入台账。用户应用后调用 query_offer_prop，将原始返回交给主 Agent，
由主 Agent 对比并决定是否需要澄清，流程见 SKILL.md 规则6。
台账继续记录任务执行结果和实际应用回执。

执行状态 `status`：

```
parsed ──确认卡确认──▶ confirmed ──开始执行──▶ running ──▶ success
   │                                                  ╰──▶ failed
   ╰──确认卡跳过──▶ skipped                                 ╰──▶ cancelled（用户终止批次）
```

应用状态 `apply_status`（独立轨道，仅 status=success 且有 item_id 的任务有意义）：

```
pending ──build_apply_card──▶ requested ──卡片回执──▶ applied / failed / unknown / cancelled
```

- `requested` 只表示「已发起批量应用卡、回执未到」；build_apply_card 后必须等卡片
  回传消息，再按回执逐任务 save_result。
- `unknown`（写入请求已提交但未能确认是否生效）**不是失败**，转述口径见 SKILL.md 规则6。
- 已 `applied` 的任务重复出现在新的 build_apply_card items 中会被组件按其防重签名
  拦截；主 Agent 应只把 pending/failed/unknown 且用户本轮点选的任务放入 items。

## 4. 主循环（主 Agent 执行口径：分批并行，每批 ≤5 任务）

确认卡回传「要执行的任务清单」并落账 confirmed/skipped（单条 bash 串联逐任务
`save_result`，每任务独立一次调用）后，主 Agent 按清单**分批并行**执行：

1. **分批**：每批 ≤5 个任务，批次间串行；`full_img_set` / `full_listing_set`
   （计划含 chain/后处理条目）建议单独成批或放批尾；`title_opt` 可混批。
2. **阶段一（启动+规划，一次迭代）**：同轮发起本批每任务一条 bash tool call，
   单条内串联 `save_result --task_id <id> --status running` 与该任务的执行技能规划
   命令（委托前先读该技能 SKILL.md）；返回的 `data.calls` 计划记录归属映射
   （tool_call_id → task_id → call_index）。
3. **阶段二（生图，全局窗口）**：本批全部任务的 calls 合并为全局队列，从队首取
   连续独立条目，全局在途 image_generate/image_edit 合计 ≤5 并行发起；遇任一任务的
   chain/deliver 条目即截断（不跨屏障凑批），该任务独立条目全部返回后下一轮单独
   发起其 chain 条目；本轮全部返回后才推进下一轮。
4. **阶段三（落账，一次迭代）**：单条 bash 串联逐任务 `save_result`：
   - 任务完成：`--task_id <id> --status success --result_summary ... --result_images ...`
     （失败：`--status failed --error <自然语言原因>`；用户终止：`--status cancelled`）
   - 每批结束用 build_result_card / Markdown 表格刷新一次进度，不逐任务刷屏；
   - **每批落账后立即向用户输出醒目进度行**（「已处理 xx%（xx/xx）—— 成功 x ·
     失败 x · 剩余 x」，计数取 save_result 返回的 data.batch_stats，skipped/cancelled
     计入已处理），再启动下一批。
5. **每处理一个任务都必须落账一次**（钉钉文档口径），不做内存累积；落账只能出现在
   单条 bash 内串联执行，**禁止**并行发起多条含 save_result 的命令（台账读改写互斥）。
6. **归位铁律**：结果按 tool_call_id → task_id → call_index 记录归属；失败/跳过条目保留
   原下标，不按返回先后、URL 或压缩成功列表匹配；单任务失败不阻断批内其他任务。
7. 执行技能内部的并发由其自身口径控制（如 image-agent 的 data.calls 每批 ≤5）；
   本节的全局窗口是跨任务调度层，两层叠加时以全局在途 ≤5 为准。

## 5. 上游交接（结构化进入批量）

上游技能（商品诊断 ONE_CLICK_OPTIMIZE、店铺体检行动项等）可直接把
`products:[{offerId, title, optimizationPoints:[{opKey, label}]}]` 结构化 JSON
交给本技能：主 Agent 将其转换为标准任务数组（opKey→op 按 §2 白名单映射，
未映射项如实报告并询问用户），经 `parse_tasks --source context --tasks` 进入台账，
后续流程与手输任务一致。
