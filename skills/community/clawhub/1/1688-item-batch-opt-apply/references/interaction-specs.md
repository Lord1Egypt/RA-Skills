# 交互组件规范（interaction-specs）

**当前主路径是 ask_user 表单，不是卡片**：batch-task-confirm / batch-result-view /
batch-apply 三个组件尚未在 1688GUI 侧开发上线，现阶段弹 `offer_select_card` 会被宿主
按默认视图渲染成商品选择卡（未知 route 回退行为），**放量前禁止弹这三张卡**。
组件上线且放量后才切换为卡片路径（本文档下半部分为届时契约，先行冻结）。

## 当前主路径（三卡组件未上线前一律走此路径）

应用前 CPV 核对以 SKILL.md 规则6 为准：展示优化全貌 → 用户应用意图 → 定向查询
query_offer_prop → 原始返回交给主 Agent 对比 → 无须澄清则沿授权通道更新商品；
需要澄清则由主 Agent 生成问题 → 用户回答后按澄清内容重新处理 → 展示完整最终方案 →
重新弹出确认应用卡片 → 用户二次确认 → 应用。查询失败/缺失不能解释为无差异。propertyNames 为模型生成的
相关匹配词，由工具内部构造正则筛选属性，避免全量 CPV 占用上下文。

第一次「应用」按钮必须回传意图并延迟写入，不能使用已经执行写入的回执触发核对。
本仓库只提供 CLI 和 Agent 流程，不实现宿主按钮/写入通道。当前逐任务 image-apply
等组件自身的确认不能由 CLI 绕过；宿主支持承接原确认的写入通道后，才可做到无差异
不再点一次。存在差异时，主 Agent 重新处理受影响内容并更新应用参数，展示完整方案后，
重新调用执行技能的确认应用卡片；该卡片承载二次确认，不沿用澄清前的旧参数。

1. **任务确认**：宿主 `ask_user`（mode=form）多选题，每题 options 2-8 个（一题最多
   列 8 个任务）、题目 1-4 个，单轮最多确认 32 个任务，超出分批；question ≤500
   字符，任务明细先在正文 Markdown 表格列清，ask_user 只做勾选确认。回执逐任务
   `save_result --status confirmed/skipped`。
2. **结果展示**：助手正文 Markdown 表格（无长度限制）+ `export_results` Excel 产物
   `present_files` 非交互式展示；`build_result_card` 的 `data.card` 落账备用不弹卡。
3. **批量应用**：逐任务执行其执行技能自己的单条目应用卡（如 image-agent 的
   `image-apply` 单卡，一次一个商品逐个确认），每弹一张后停轮等回执，回执逐任务
   落账 apply_status。逐个确认成本高时先向用户说明「需逐个确认」。

## MCP App 卡片调用硬约束（所有 offer_select_card 弹卡通用，含当前逐任务单卡与升级路径三卡）

与 1688-item-image-agent 的卡片调用硬约束一致（端侧代码：phoenix-pc 的
accio-widget-registry / mcp-app-presenter 渲染链路）。

1. 必须用 Bash **直接执行** `accio-mcp-cli call --server accio offer_select_card --json '<参数>'`；
   Windows 用 `--json-file "<绝对路径>"`（参数 JSON 先写入系统临时目录 UTF-8 文件）。
2. **不加 `--raw`、不接管道、不包在 Python 或 cli.py 里**；否则宿主不渲染卡片。
3. 弹卡命令必须是本轮最后一个工具调用；调用后只输出一句不断言「已弹出」的引导语
   （如“已发起任务确认卡，请在卡片中勾选要执行的任务”）并立即结束本轮。
   退出码 0 不代表卡片已显示；命令报错/超时按「卡片加载失败」如实告知，不自动重试。
4. 用户在卡片中提交后，结果作为**一条新的用户消息**到达；只从该消息读取选择/回执，
   不编造、不从其他上下文猜测。
5. 卡片回传中的内部字段（图片 URL、store_ref、签名等）仅作内部参数，禁止在面向
   用户的回复、进度、总结或错误说明中复述或展示。
6. 用户明确要求「重新弹出」时视为新指令，可重新弹卡（batch-apply 前需重跑
   build_apply_card）。

## batch-task-confirm（任务确认卡，升级路径）

```bash
accio-mcp-cli call --server accio offer_select_card --json '<parse_tasks.data.confirm_card>'
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `route` | 是 | 固定 `batch-task-confirm` |
| `batchSize` | 是 | 待确认任务数 |
| `tasks[]` | 是 | 每任务 `taskId/itemId/itemTitle/mainImage/op/opLabel/requirements`；`mainImage` 留空由组件取图 |

- 展示 item_id、主图、解析出的属性字段，支持多选/全选/反选、分页或滚动
  （钉钉文档「任务解析及确认」）。
- 回执消息应包含用户勾选的 taskId 清单与被跳过的 taskId 清单；主 Agent 据此
  `save_result --status confirmed/skipped` 逐任务落账后进入执行。
- 取消/空回执：停止执行，如实说明；不把 parsed 任务默认执行。

## batch-result-view（执行结果展示卡，升级路径）

```bash
accio-mcp-cli call --server accio offer_select_card --json '<build_result_card.data.card>'
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `route` | 是 | 固定 `batch-result-view` |
| `batchId` | 是 | 批次 ID |
| `progress` | 是 | `{total, done, success, failed, skipped}` 进度统计 |
| `tasks[]` | 是 | 每任务结果条目（含 `resultSummary/applyStatus/applyDetail/error`） |
| `appliableTaskIds[]` | 是 | 可进入应用环节的 taskId（执行成功且未应用） |

- 进度展示与逐任务结果合并展示；执行过程中可多次弹卡（建议每完成若干任务或
  批次收尾时刷新一次），组件按 batchId 幂等更新。
- 卡片上的「应用到商品」入口：用户点击后回执消息表达应用意图（可含勾选的
  taskId），主 Agent 走 SKILL.md 规则6 进入应用环节。

## batch-apply（批量应用确认卡，升级路径）

```bash
accio-mcp-cli call --server accio offer_select_card --json '<build_apply_card.data.card>'
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `route` | 是 | 固定 `batch-apply` |
| `batchId` | 是 | 批次 ID |
| `items[]` | 是 | 每条目 `taskId/itemId/itemTitle/op/opLabel/applyParams`；`applyParams` 为执行技能单条目应用参数原样透传（如 image-agent `prepare_image_apply.data.card_params`） |
| `defaultApplied` | 是 | 固定 `false`：每项默认不应用 |

- **每项默认不应用**；用户在卡片中逐项开关/反选、全部应用/全部不应用，确认后
  由组件一次性完成写入（写入能力只在组件侧，Agent 与 CLI 均不写商品）。
- 回执消息应包含逐条目（taskId 粒度）的成功、失败明细与原因；主 Agent 按回执
  逐任务 `save_result --apply_status applied/failed/unknown/cancelled --apply_detail ...`。
- 状态未知/处理中按 `unknown` 落账：不是失败，转述口径见 SKILL.md 规则6。
- 卡片不可用（组件未上线/灰度未放量）时：回退为逐任务单条目应用（对每个任务
  原样执行其执行技能的 image-apply 单卡流程），并如实告知用户将逐个确认。

## 组件能力位与放量切换

batch-task-confirm / batch-result-view / batch-apply 为 1688GUI 侧新组件（MCPAPP）。
宿主对未注册的视图名走透传分支、写入视图必须先登记进写入视图拦闸
（ACCIO_WRITE_WIDGET_VIEWS）才能放开下发。三卡放量前一律走上文当前主路径；
宿主/端侧放量公告确认后再切换为卡片路径，切换后原主路径转为卡片加载失败时的
兜底链路。任何链路切换或降级发生时如实告知用户，不得静默假装卡片已展示。
