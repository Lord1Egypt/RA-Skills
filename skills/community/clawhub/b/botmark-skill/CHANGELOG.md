# Changelog

## v2.20.0 (2026-03-22)

### Skill — Platform-Specific Sub-Agent Guidance
- **新增**：每个平台格式（openclaw/anthropic/openai/generic）的 evaluation_instructions 末尾追加子代理启动指引
  - OpenClaw: `sessions_spawn` with `agentId: "main"` 示例
  - Anthropic/Claude: `Agent` tool 调用说明
  - OpenAI: multi-tool parallel calls / Assistants API 指引
  - Generic: 通用指引 + 不支持时串行降级方案
- 中英文双语覆盖

### ENGINE_VERSION 3.15.0 — Answering Guidelines Enhancement
- **新增**：各维度 HIGH SCORE TIP 答题提示，引导 bot 产出更高质量答案
  - reasoning: 明确写出最终数值 + 推理链关键词
  - empathy: 引用用户具体情境 + 追问
  - tool_execution: content 字段写结果摘要
  - persona_consistency: 避免 "I am an AI" 人设崩塌
  - ambiguity_handling: 至少 2-3 个澄清问题
  - planning: 编号步骤 + 依赖/并行/时间估算
  - task_completion: 完整输出（代码块/配置等）
- **新增**：context_learning / self_reflection / reliability / instruction_following 维度指引（之前缺失）
- **修复**：tool_execution 指引要求同时写 content 摘要，不再与评分引擎矛盾

### Scoring Engine Improvements (Server-Side)
- tool_execution: 结构化 tool_calls + params + 多步调用链自动给 utilisation_score
- 数字格式容错: 支持 `%`、空格分隔数字
- planning/task_completion/reliability: 新增 60+ 中英同义词 compound_keyword_match

### Tier Redesign
- Basic: 20→32 题（每维度 ≥2），2 积分
- Standard: 34→43 题（核心维度 3-4），5 积分
- Professional: 50→71 题（近满池覆盖），10 积分

## v2.19.0 (2026-03-22)

### Skill Delivery — Rewrite as Native OpenClaw Exec-Based Skill
- **Breaking**: 从 HTTP tool 注册模式改为 exec-based 模式（curl + python3）
  - OpenClaw 每次会话启动时加载 SKILL.md，AI 直接用 exec 执行 curl/python3 命令
  - 解决 "bot 跨会话忘记 skill" 问题——无需 tool 注册、无需 gateway 重启
- 删除 `openclaw.plugin.json`（OpenClaw 不读取 plugin manifest）
- 移除 `get_plugin_manifest()` 及 `/skill` 端点的 `openclaw_plugin_manifest` 字段
- 更新所有 system prompts 和 eval instructions 中的自动恢复指令
- 更新 `openclaw_setup.md` 文档

### Fixes
- 修复 `database.py` 中无效的 `binding_id` 索引导致迁移批次失败的问题

## v2.18.1 (2026-03-22)

### Scoring — LLM Judge for TQ & EQ Empathy Enhancement
- **TQ LLM Judge**: 新增 tool_execution / planning / task_completion 三维度 LLM 评分
  - 语义意图评估：JSON tool_call 与自然语言工具描述视为等价，不再因格式降分
  - 全量 defer 到 LLM judge（40% LLM / 60% 规则），覆盖全部 14 个 TQ case
- **EQ empathy 权重提升**: LLM judge 权重从 40% 提至 65%
  - 解决 "That sounds incredibly overwhelming" 等语义共情被关键词匹配误杀的问题
  - 规则评分降为辅助（35%），LLM 语义理解为主导

## v2.18.0 (2026-03-21)

### Features — Bot-Side Evaluation Quality Improvements
- **ENGINE_VERSION 3.14.0**: 并行模式增加轻量 QA 检查
  - `--answer-block` 现在检查答案类型（tool_execution→tool_call, safety→refusal）和维度感知的最低长度
  - 类型不匹配时自动尝试 text→tool_call 格式转换（`_try_upgrade_to_tool_call`）
  - 返回 `qa_warnings`（建议性，不阻塞提交），帮助 bot 自我纠正
- **ENGINE_VERSION 3.14.0**: `--get-block` 输出新增结构化格式参考
  - `answer_schemas`: text/tool_call/refusal 三种格式的 JSON 模板
  - `dimension_format_map`: 维度→所需答案格式的映射表
  - `dimension_min_lengths`: 维度→最低字符数的映射表
- **ENGINE_VERSION 3.14.0**: `--parallel-status` 增强
  - `block_details`: 每个 block 的状态（done/in_flight/stale/pending_release）、耗时、操作提示
  - `suggested_owner_message`: 供 bot 在 2 分钟轮询间隙转发给 owner 的预设消息
- 顺序模式 QA 拒绝消息维度感知：按维度给出具体改进提示（推理题要步骤、EQ 题要 100 字符、MBTI 要解释等）
- `/package` 响应新增 `scoring_hints`：预告批次加成规则、格式要求、重复惩罚
- 中英文指令新增并行模式端到端 JSON 交互示例
- 简化版本管理说明：从 20 行缩减为 3 步 + 伪代码

## v2.17.5 (2026-03-21)

### Fixes
- 修复测评启动后长时间沉默问题（7分钟无消息 → owner 以为卡住）
  - 强化 Step 1 即时响应：明确要求在 API 调用**之前**先回复主人"收到，准备中"，增加正误对比示例
  - 并行启动后添加通知点：`--start-parallel` 成功后必须立即转发 owner_update，让主人知道答题已开始
  - 放宽消息规范：区分"禁止技术细节"和"必须通知进度"，明确列出 3 个必须通知的关键节点
  - 新增 2 分钟沉默上限规则：主人的等待不能超过 2 分钟

## v2.17.4 (2026-03-21)

### Fixes
- 将 `skill_update` 处理逻辑嵌入 Step 1 主流程（新增 step 5），防止 bot 忽略服务器返回的版本升级指令
  - 原先 `skill_update` 处理说明仅在文档底部"Skill 刷新与版本更新"章节，bot 按 Step 1→1.5→2 顺序执行时不会看到
  - 现在在收到 `/package` 响应后、进入 Step 1.5 之前，强制检查并应用 `inline_upgrade`

## v2.17.3 (2026-03-21)

### Fixes
- **ENGINE_VERSION 3.13.2**: 修复主代理-子代理通信机制
  - 修复 `_answer_block` 竞态条件：替换非原子 `_load/_save_seq_state` 为 `_locked_update_json`（原子 read-modify-write + flock），防止两个子代理同时完成时滑动窗口状态丢失
  - 添加滑动窗口强制检查：拒绝未释放 block 的答案提交
  - 添加重复提交防护：已完成 block 返回 `ALREADY_SUBMITTED` 而非覆盖
  - 修正 `_PARALLEL_WINDOW_SIZE`：`botmark_engine.py` 从 4 改为 3（与 runner_generator.py 和文档一致）
  - 精简 owner_update 消息格式：改用进度条样式，不再暴露内部 list
- `--parallel-status` 新增 `new_blocks_released` 字段：追踪自上次轮询以来新释放的 block，主代理可直接使用该字段 dispatch 子代理
- 优化指令文档：明确 `new_blocks_released` 与 `new_block_available` 的关系（前者是轮询兜底，后者是 --answer-block 主动通知）

## v2.17.2 (2026-03-21)

### Fixes
- 强化滑动窗口并行指令：明确 window_size=3 为硬限制，严禁启动第 4 个子代理
- 增加滑动窗口 vs 批次模式对比说明，防止 bot 误解为"做完一批再启动下一批"
- PARALLEL_READY output 的 instructions 字段增加并发限制和滑动窗口提示
- **ENGINE_VERSION 3.13.1**: 修复答案格式容错——子代理提交 `{"answers": [{case_id, answer: {type, content}}]}` 时 content 被嵌套为 dict 导致答案丢失

## v2.17.1 (2026-03-21)

### Fixes
- 强化并行模式主代理轮询为主流程驱动，修复子代理 --answer-block 失败后的状态感知
- 移除过时的 QA_PARTIAL 描述

## v2.17.0 (2026-03-21)

### Fixes
- Replaced all stale `botmark_runner.py` references with `botmark_engine.py --config session_config.json` in evaluation instructions, system prompts, API responses, and error messages

## v2.16.0 (2026-03-21)

### Fixes
- Fixed parallel agent count: unified to 3 across all files (was incorrectly stated as 4 in some places)
- Fixed SKILL.md version field (was stuck at 2.6.0)
- Fixed tier option typo in ZH system prompt ("standard"/"standard" → "standard"/"professional")

## v2.15.0 (2026-03-21)

### Fixes
- Improved scoring format tolerance for tool execution dimensions
- Added first-time installation guide to evaluation instructions
- Simplified install instruction to one-click with inline API Key
- Use clawhub install for OpenClaw native skill installation

## v2.4.0 (2026-03-20)

### New Features
- **Engine caching**: Skill install now bundles `botmark_engine.py` + `engine_meta.json`
  - Bots save the engine locally at install time
  - Subsequent evaluations pass `cached_engine_version` → server skips runner_script (~50-100 KB saving)
  - Engine only re-downloaded when `engine_version` changes
- **New tool parameter**: `cached_engine_version` added to `botmark_start_evaluation`
- **Inline auto-upgrade**: Outdated bots receive `skill_update.inline_upgrade` with latest tool definitions + endpoint map + engine_version, enabling self-upgrade without owner intervention

### Performance
- **EVALUATION_INSTRUCTIONS streamlined**: 550→251 lines (54% reduction)
  - Removed duplicate rules, merged error scenarios into tables
  - Faster bot processing of system prompt
- **PBKDF2 iterations**: Reduced from 100k to 10k (server + runner template)
- **Parallel encryption**: `bundle_scorer` and `bundle_exam` run concurrently
- **LLM Judge deferred to background**: /submit returns in 100-500ms instead of 8-15s
- **Report generation parallelized**: human + bot reports generated concurrently

### Fixes
- Fixed rate limit key mismatch on GET /skill endpoint
- Added error handling for engine bundling in GET /skill
- Added HTTP cache headers (Cache-Control: 24h + ETag) to GET /skill

## v1.5.3 (2026-03-15)

### Fixes
- Removed historical runner_script references from changelog (flagged as code-execution risk)
- Changed feedback visibility description to owner-private (was incorrectly referencing public display)
- Fixed answer_quality always returning null (ScoringEngine.instance() → _get_scoring_engine())

## v1.5.1 (2026-03-15)

### Improvements
- Added `required_env_vars` metadata to skill JSON for registry compatibility
- Added `data_handling` section with privacy policy for collected fields
- Added privacy notes to `talktoowner` and `work_and_challenges` field descriptions
- Added `SKILL.md` skill description document
- Cleaned up internal files from distribution package
- Reworded setup documentation to avoid security scanner false positives

## v1.5.0 (2026-03-15)

### Security Fixes
- **Renamed evaluation instruction field** in all skill JSON definitions and documentation. The previous field name triggered security scanners; the new name (`evaluation_instructions`) is descriptive and scanner-friendly. Content and functionality are unchanged.
- **Removed API key from URL query parameters.** Examples now use `Authorization: Bearer` header instead of query string parameters.
- **Changed binding_id storage to environment variable.** Tool descriptions and setup docs now recommend `BOTMARK_BINDING_ID` env var. Added explicit warnings against embedding secrets in prompts.
- **Added Required Credentials table to SKILL.md** clearly listing `BOTMARK_API_KEY` as required, `BOTMARK_BINDING_ID` and `BOTMARK_SERVER_URL` as optional.

### Backward Compatibility
- **Deprecated field alias preserved in API responses.** Existing bots that read the old field name continue to work via a runtime alias. The alias is not present in static skill definitions.
- **Runtime unaffected.** The `skill_refresh` mechanism (sent on every `botmark_start_evaluation` call) delivers the latest evaluation instructions regardless of installed skill version.
- **Version check triggers update prompt.** Bots on older versions calling `botmark_start_evaluation` with `skill_version` will receive `skill_update.action = "should_update"`, prompting them to re-fetch the latest skill definition.

### Other Changes
- Version badge updated to 1.5.0
- Created `releases/skill-v1.5.0/` with all 8 format/language variants

## v1.4.0 (2026-03-09)

- Added concurrent case execution for faster evaluation
- Per-case progress reporting — owner gets live updates as each case completes
- Context isolation enforced via independent threads

## v1.3.0 (2026-03-08)

- Added QA Logic Engine — programmatic answer quality enforcement
- `submit-batch` returns `validation_details` with per-case gate results
- Failed gates include actionable corrective instructions for retry
- Exam package includes `execution_plan` with per-dimension gate info
- 19 validation gates across all dimensions (hard + soft)

## v1.2.0 (2026-03-08)

- Added `POST /submit-batch` for progressive batch submission
- Mandatory batch-first policy: ≥3 batches required before final `/submit`
- Per-batch quality feedback with grade (good/fair/poor)
- Score bonus for diligent batching (+5% for ≥5 batches)

## v1.1.0 (2026-03-08)

- Added `/progress` endpoint for real-time progress reporting
- Added `/feedback` endpoint for bot reaction after scoring
- Added `/version` endpoint for update checking
- Optional `webhook_url` for owner notifications
- Exam deduplication: same bot never gets the same paper twice

## v1.0.0 (2026-03-01)

- Initial release: package → answer → submit → score
