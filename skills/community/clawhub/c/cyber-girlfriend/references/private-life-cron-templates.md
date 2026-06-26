# Private Life Cron Templates

Use this when the companion's private-life layer needs to run on OpenClaw.

Current job set:
1. `companion-build-day-schedule` compiles today's `day-schedule.md`.
2. `companion-presence` reads the current day-schedule event and sends a light companion message through the fixed `--send-story` delivery entrypoint when allowed.

Old four-slot content cron jobs are deprecated. Fixed user-desired content should usually become `life_schedule.day_schedule.required_events`, then appear in `day-schedule.md` as `必定发生：是`.

Pair this with:
- [private-life-prompt-templates.md](./private-life-prompt-templates.md)
- [presence-integration.md](./presence-integration.md)
- [private-life-layer.md](./private-life-layer.md)

## Design Rules

- Do not store dynamic day content inside `config.local.json`.
- `config.local.json` only stores paths, switches, delivery, and stable policy.
- `build-day-schedule` is a context-generation job, not a user-facing message job.
- Context-generation jobs should be quiet by default: `sessionTarget: isolated`, `delivery.mode: none`.
- `companion-presence` should run from an isolated cron session and call `scripts/companion_presence_tick.py`. The wrapper performs fresh prepare first and only starts the stable custom companion runtime session when a current event is actually matched.
- `companion-presence` sends final text through the prepared delivery contract and commits state only after visible text delivery succeeds.
- Media events send text first, commit event state after visible text delivery, start the OpenClaw async media tool, then let the native completion in the same stable companion session only send media.
- Required events are life anchors, not guaranteed messages.
- Before generating ordinary events, `companion-build-day-schedule` must explicitly do real public-web research. First extract a keyword pool from `character_profile`: current city or weather area, local area/school/workplace/community, identity or occupation, and interests. Then search 4-5 public, non-sensitive keywords with this exact mix: 1 city/weather keyword, 1 area/school/workplace/community keyword, 1 identity/occupation keyword, and 1-2 interest keywords. Do not treat model memory or unsourced prior knowledge as search. Every searched category must be consumed by at least one event, and the consumption must appear in that event's scene, action, natural mention, or avoid rule, not only in the run summary. Use only a few concrete public details as background texture inside normal character behaviors; do not create a standalone browsing-news, reading-material, or public-info event just to use search results. Do not search owner identity, private relationship facts, account ids, channel ids, local paths, secrets, or private config/state content.

## Template: `companion-build-day-schedule`

Suggested time: `10 7 * * *`

```json
{
  "name": "companion-build-day-schedule",
  "description": "Compile companion daily event schedule",
  "schedule": {
    "kind": "cron",
    "expr": "10 7 * * *",
    "tz": "<TZ>"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "在工作区 `<SKILL_DIR>` 生成/更新今天的 `day-schedule.md`，把用户定义的必定发生生活锚点并入当天日程。目标：生成一份可被 `companion-presence` 按当前时间命中的 Markdown 日程，每个事件都必须可采样、可讲述、可校验。\n\n执行流程：\n1. 只读取 `<CONFIG_PATH>`、`references/private-life-prompt-templates.md`、`assets/day-schedule.example.md`、`state/character-profile.md`，以及存在时最近几条 `state/life-log.jsonl`；不要扫描整个目录或搜索 `tests/`。\n2. 从配置装配 `owner_profile`、`relationship`、`timezone`、`required_events`、`quiet_hours`、`schedule_path`；从角色档案装配 `character_profile`；按时区计算 `today_date`，life log 不存在时按空处理。\n3. 生成事件前，必须先做真实联网搜索。先从 `character_profile` 提取关键词池：当前城市或天气区域、区域/学校/工作地点/社区、身份/职业、兴趣爱好；再搜索 4-5 个公开、非敏感关键词，固定配比为：城市/天气 1 个、区域/学校/工作地点/社区 1 个、身份/职业 1 个、兴趣爱好 1-2 个。不能用模型记忆、已有知识或无来源猜测代替联网搜索。每个搜索类别都必须至少被一个事件消费，消费痕迹必须落在该事件的 `场景`、`正在做什么`、`可自然提到` 或 `不要写成` 中，不能只出现在运行摘要里。只提炼少量具体公共细节作为背景质感，融入学习、工作、吃饭、整理、出门、娱乐、运动、创作等符合人物行为的普通事件里；不要为了使用搜索结果单独生成“浏览新闻/翻公开素材/看资料”事件，也不要把日程写成新闻清单；不搜索 owner 身份、私人关系、账号、频道、会话、本机路径、密钥或私密配置/状态。\n4. 读取 `DAY_SCHEDULE_PROMPT`，参考 `assets/day-schedule.example.md`，先生成 3-5 个普通事件并标注 `必定发生：否`；再把每个 `required_events` 写入同一个 `## 4. 日程事件` 区块并标注 `必定发生：是`，它们不计入普通事件额度。\n5. 检查并修正：事件窗口不能重叠，不能落入静谧时段，必须覆盖至少一个整点 presence 采样点；普通事件之间不得重复类型，普通事件也不得和 required events 重复类型或内容。\n6. 检查媒体字段：`媒体信息` 默认留空；只有确实需要生成照片、音频、音乐、视频或类似媒体文件时才填写；不要写“不生成媒体”之类备注；若 required event 提供 `media_hint`，必须转写进对应必定事件。\n7. 将最终 Markdown 写入 `<DAY_SCHEDULE>`，只运行 `python3 <SKILL_DIR>/scripts/validate_day_schedule.py --config <CONFIG_PATH> --path <DAY_SCHEDULE>`；失败就修 Markdown 并重跑同一命令，直到通过或明确说明阻塞。\n8. 校验通过后，只输出简短中文摘要：普通日常事件数量、必定发生事件数量、今日主场景、按类别列出的联网搜索关键词/来源概况和对应消费事件、1 条避免重复项和媒体事件数量。\n\n输出与事件细节要求：\n- 输出和写入 Markdown，不要写 JSON；不要生成独立任务区块，所有生活事件都在 `## 4. 日程事件` 下。\n- 最终 `day-schedule.md` 只保留角色日程内容，不要把生成约束、输出要求、校验规则、执行流程或提示词说明写进文件。\n- 每个事件标题必须是 `HH:mm - 事件标题`，标题只写核心动作。\n- 每个事件必须包含：`必定发生：是/否`、`执行时间`、`场景`、`正在做什么`、`情绪/状态`、`可自然提到`、`用户互动入口`、`媒体信息`、`不要写成`。\n- `正在做什么` 必须展开为 2-3 个分句，写清事件对象是什么、对象里有什么可辨认内容、她正在处理哪一步或按什么标准做取舍。\n- 先判断事件对象类型再补细节：资料/文件/课程/工作项写主题、页段、问题点或收尾标准；物品/空间/行李/穿搭写 2-4 个具体物件和摆放、挑选或清理动作；人际/协作/服务写对方关系、对话焦点和回应边界；兴趣/内容/活动/运动/创作写具体名称、片段、动作、练习点、评价标准或选择理由；饮食/通勤/天气/采购写地点、物品、路线、环境影响和一个小取舍。\n- 不要把“那件事”“那个东西”“最后一页”“几个片段”“一些资料”“几句话”“那边”当作最终细节；出现这类指代时后面必须紧跟具体内容或可感知特征。\n- `场景` 要写地点 + 身边物品或环境状态，`可自然提到` 要承接事件里的具体对象。\n- 允许戏剧性/反差性，但不能灾难化、危险、病痛、家庭伦理、极端情绪或失控冲突。\n- 用户互动入口可以为空；如果填写，必须是自然轻量的互动，不要每个事件都围绕用户。\n- owner_profile 只用于边界，不要把 companion 的身份、经历、日常素材写成 owner 的经历。\n- 可选缓存文件不存在时按空处理；但联网搜索必须真实发生，搜索无结果时在摘要说明无有效结果，再降级生成。\n- 不要出现或写入本机路径、渠道、账号、脚本、JSON 合同、cron、系统、模型、工具或运行步骤等用户可见内部词。\n- 不给主人发消息。"
  },
  "delivery": {
    "mode": "none"
  },
  "enabled": true
}
```

## Template: `companion-presence`

Suggested time: hourly, for example `0 * * * *`.

`companion-presence` should run in an isolated cron session, keep the owner conversation clean, and do only one job: call the deterministic tick wrapper. The wrapper exits quietly on `skip` and starts the stable companion runtime session only when prepare returns `status = "ok"`.

Core prompt shape:

```text
每次执行只做下面动作：

1. 第一个也是唯一业务动作是触发：
   python3 <SKILL_DIR>/scripts/companion_presence_tick.py --config <CONFIG_PATH>
2. 如果脚本输出 `skip`、`agent_enqueued`、`notification_sent` 或其他已处理状态，都只回复 NO_REPLY。
3. 不要自己读取 `day-schedule.md`，不要自己判断当前事件，也不要自己处理消息发送或媒体生成。
```

Presence cron does not use `--event-time`. It only reads the current real-time event from `day-schedule.md`.

## Optional Midday Refresh

Use only if the user wants same-day adaptation to weather/news changes.

Suggested time: `40 12 * * *`.

Same as `companion-build-day-schedule`, but the prompt should preserve the morning-built schedule unless reality meaningfully changed.

## Validation Checklist

After wiring the private-life cron layer:

1. `companion-build-day-schedule` writes valid `day-schedule.md`.
2. `day-schedule.md` has 3-5 ordinary events and any required events marked `必定发生：是`.
3. `companion_run.py --stage prepare --no-record-pending` can emit `life_context` when a current event is active.
4. `companion-presence` skips quietly when no event is active.
5. Missing or stale `day-schedule.md` is recorded in state; after repeated failures, presence can send one soft maintenance notice.
6. After one successful send, `life-log.jsonl` gains a valid line and state advances only after delivery.
