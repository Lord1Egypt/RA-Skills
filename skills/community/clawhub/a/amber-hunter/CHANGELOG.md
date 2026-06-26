## [v1.2.41] — 2026-04-09

### Added
- **BGE-M3 Embedding** — `core/embedding.py` 新增 `BGEProvider` 类，支持 BAAI/bge-m3（1024-dim，多语言）；`encode_chunks(text)` 方法支持按句子边界分块
- **BM25 关键词检索** — `core/bm25.py` 新建 `BM25Searcher` 类，使用 rank_bm25 库；recall 在 keyword/hybrid 模式下自动启用 BM25 增强关键词匹配
- **Cross-Encoder Reranker** — `core/reranker.py` 新建 `Reranker` 类，使用 BAAI/bge-reranker-v2-m3 本地模型；`rerank_engine=model` 时调用
- **HyDE 支持** — `core/hyde.py` 新建 `HyDEGenerator` 类，用 LLM 生成假设性答案增强检索；`hyde=True` 参数启用
- **Multi-Hop 检索** — 多跳推理支持，从种子胶囊扩展查询；`multi_hop=True` 参数启用
- **`POST /recall/evaluate`** — RAG 评测端点，使用 RAGAS 框架计算 faithfulness/answer_relevancy/context_precision + NDCG@5
- **`benchmark/recall_eval.py`** — RAG 评测工具，输出 `benchmark/results/recall_eval_<timestamp>.json`

### Changed
- **Embedding 模型升级** — 默认从 all-MiniLM-L6-v2 (384-dim) 升级到 BAAI/bge-m3 (1024-dim)
- **config.json** — 新增 `embed_model`、`embed_dimension`、`rerank_model`、`bm25_enabled`、`chunk_size`、`chunk_overlap`、`hyde_enabled`、`multi_hop_enabled` 配置项
- **/recall 响应** — 新增 `rerank_time_ms`、`hyde_time_ms`、`retrieval_hops` 字段

### Fixed
- **向后兼容** — 所有新参数均有默认值，原有调用不受影响；BM25/Reranker/HyDE 默认关闭

## [v1.2.40] — 2026-04-08

### Fixed
- **P0: 语义模型从未真正加载** — `_get_embed_model()` 和 `_preload_embed_model()` 均只创建 Provider 实例但未触发 `SentenceTransformer` 实际加载；现已对两个函数均加入 `provider.encode(["..."])` 强制热启动，并正确更新 `_EMBED_MODEL` 全局变量；`/status` 的 `semantic_model_loaded: true` / `semantic_model_state: "ready"` 现在正确反映状态
- **P2: Vector DB size 始终显示 0** — `get_vector_stats()` 用 `iterdir()` 只扫描顶层文件，LanceDB 数据实际存储在 `capsule_vectors.lance/` 子目录的多层 version 文件夹中；改为 `os.walk()` 递归计算，1698 条向量正确显示 141.41 MB

### Added
- **文档修正** — SKILL.md `/recall` API 参数 `query` → `q`（与实际 API 一致）

### Changed
- **版本统一** — amber_hunter.py 3处版本号（FastAPI app、/status、/root）统一为 v1.2.40
- **SKILL.md version** → 1.2.40

## [v1.2.39] — 2026-04-07

### Added
- **Temporal validity** — `valid_from`/`valid_to` columns on capsules (schema migration)
- **Contradiction Detection** — `core/contradiction.py` detects fact conflicts before ingest:
  - Date/time parsing: `since 2022`, `2021 to 2023`, `3 years ago`, `Jan 2024`
  - Entity extraction: `team_size`, `years_exp`, `start_year`, `db_type`, `project_status`
  - Conflict rules: ≥2 person difference, ≥1 year difference, any start year conflict
- **`/ingest` → contradiction check** — direct-write path (confidence≥0.95) and queue approve both run `check_contradiction_on_ingest()`; warnings returned in API response
- **`/extract/auto` → contradiction check** — auto-extract now runs contradiction detection with `valid_from`/`valid_to` and category_path inference
- **Claude Code hooks** — `hooks/amber_save_hook.sh` (Stop hook, every 15 exchanges) + `hooks/amber_precompact_hook.sh` (PreCompact hook, emergency save)

### Changed
- `insert_capsule()` gains `valid_from`/`valid_to` keyword args

## [v1.2.38] — 2026-04-07

### Added
- **Knowledge Compiler** — `core/wiki_compiler.py` 生成带 `[[capsule_id:topic]]` wikilinks 的 markdown concept page
- **`GET /concepts`** — 列出所有 concept pages
- **`GET /concepts/<path>`** — 获取指定 path 的完整 wiki markdown
- **`POST /admin/compile`** — 手动触发 concept page 编译（单 path 或批量覆盖缺口）
- **`GET /admin/compile/status`** — 查看编译状态 + 覆盖缺口列表
- **Daemon** — `start_compile_daemon(interval_hours=6.0, capsule_threshold=100)` 后台自动编译
- **wikilinks 代码事后注入** — LLM 生成 wikilinks 不稳定，改为 post-process 拼接

### Changed
- `insights` 表新增 `concept_slug`/`wiki_content` 列（向后兼容 migration）
- `generate_insight()` 改用 `_generate_wiki_insight()` 生成 wiki markdown

### Fixed
- `core/extractor.py` — 跳过空白 memo 防止空胶囊入库

## [v1.2.22] — 2026-04-04

### Added
- **D2: DID Challenge-Response auth** — `POST /did/auth/challenge` + `/did/auth/sign-challenge` client-side endpoints
- **D2: Capsule encryption via DID key** — `create_capsule`/`get_capsule`/`_do_sync_capsules` wire `derive_capsule_key` (DID device_priv → HMAC-SHA256 → AES-256-GCM), PBKDF2 fallback

### Fixed
- Fix `row[2]` vs `challenge` bug in cloud `/api/did/auth/verify` (line 1570)
- Fix `did_register_device` using wrong token (raw local token → `get_api_token()`)
- Fix `HOME` reference before definition (line 656)
- Fix `did.py` not deployed to VPS (required for Ed25519 verification)

## [v1.2.20] — 2026-04-04

### Added
- **A2: DID multi-device identity** — BIP-39 mnemonic → Ed25519 identity keypair + device key; `POST /did/setup` (generates + saves to did.json), `GET /did/status`, `POST /did/register-device`

## [v1.2.19] — 2026-04-04

### Added
- **B3: Proactive intent prediction** — handler.js scene detection (SCENES/detectScene/loadPreloadMemories/writePreloadFile), `GET /session/preload` returns context-aware memories before AI responds

## [v1.2.18] — 2026-04-04

### Added
- **B2: Insight cache compression** — `insights` table stores LLM-compressed summaries per category_path; `GET /admin/generate-insights`; `GET /recall?use_insights=true` prioritizes insight cache over full capsule scan

## [v1.2.17] — 2026-04-04

### Fixed
- **P0-1: proactive capture 字段映射错误** — `handler.ts/js` 发送 `content` 但 IngestIn 期待 `context`；`memo` 从正则匹配文本改为完整句子；`snippet` 现在正确传入 `context` 字段；解决了琥珀只有一句话、没有上下文的问题

## [v1.2.16] — 2026-04-04

### Added
- **/config GET 返回 `sync_interval_minutes`** — 云端同步间隔可配置（默认 30 分钟）
- **/config POST 支持 `sync_interval_minutes`** — 持久化到 config，下次启动生效

### Testing
- **test_sync.py 新增 4 个可靠性测试** — `TestSyncReliability`: partial_info / retry / concurrent_guard / exception_reporting

## [v1.2.15] — 2026-04-03

### Fixed
- **P0-1: `update_capsule` 重置 `synced=0`** — 编辑胶囊后本地修改现在会重新进入待同步队列，修复幽灵同步 bug；`updated_at` 字段同步更新
- **P0-2: `updated_at` 字段** — 胶囊新增 `updated_at` 列（core/db.py + amber_hunter.py），为云端冲突检测打下基础
- **P1-4: 同步重试逻辑** — `_do_sync_capsules` 对 5xx 错误最多重试 2 次（指数退避 1s/2s），4xx 和异常立即失败不重试；修复 `elif attempt < 2` 条件在 attempt=2 时错误跳过重试的逻辑 bug
- **P1-5: `get_unsynced_capsules` 加 `ORDER BY`** — 未同步胶囊按 `created_at ASC` 排序（先老后新），配合批次处理保证顺序一致性
- **P1-6: 同步并发控制** — `_spawn_sync_if_enabled` 加线程锁（`threading.Lock`），防止多个同步线程同时运行导致重复上传
- **P1-7: 后台同步异常上报** — `_background_sync` 异常写入 `config.sync_last_error`，`/status` 端点返回 `sync_last_error` 字段
- **P2-8: `update_capsule` 使用 thread-local 连接** — 改用 `_get_conn()` 复用连接池而非独立 `sqlite3.connect`
- **P2-9: 同步前网络可达性预检** — 同步前用 `socket.create_connection` 检查 huper.org 443 端口，不可达则立即返回避免无用尝试
- **P2-10: `get_unsynced_capsules` 加 `ORDER BY created_at ASC`** — 保证胶囊按创建顺序上传
- **P3-11: `last_sync_at` 独立记录** — 同步完成后用 `set_config("last_sync_at", timestamp)` 而非 `MAX(created_at)`，保证 `last_sync` 时间精确
- **P3-13: 同步间隔可配置** — 定时同步从 config 读取 `sync_interval_minutes`（默认 30 分钟），Dashboard 可动态调整
- **`CapsuleUpdate` 未导入** — 修复 `update_capsule` 函数因缺少 `from core.models import CapsuleIn, CapsuleUpdate` 导致 FastAPI OpenAPI schema 生成失败（返回 422）

### Changed
- **P0-3: `sync_to_cloud` 返回值增强** — 返回 `failed`（失败数）、`partial`（是否有部分失败）、`all_synced`（是否全部成功）字段，Dashboard 可精准展示同步状态
- **`/status` 端点** — 新增 `sync_last_error` 字段（来自 config 表），Dashboard 可展示最近同步错误
- **`_do_sync_capsules` 重构** — 简化重试逻辑结构，消除嵌套 for-else歧义；`for attempt in range(3)` 替代 `while` 循环，代码更清晰

---

## [v1.2.13] — 2026-04-03

### Added
- **语义模型状态细化** — `/status` 返回 `semantic_model_state`（loading/ready/error/unavailable）+ `semantic_model_error`；recall semantic/hybrid 模式若模型正在加载返回 503 + `MODEL_LOADING` code
- **启动预加载语义模型** — `main()` 末尾调用 `_preload_embed_model()` 后台线程预加载，减少首次语义搜索延迟
- **E2E测试框架** — `tests/` 目录，pytest + pytest-asyncio + pytest-mock；覆盖 crypto roundtrip、recall 两阶段解密、/status 端点

### Changed
- **统一信号体系** — handler.ts/js 信号类型统一为 6 种（save_request/decision/preference/personal_fact/summary/insight）；修复 POST 路径 `/capsules` → `/ingest`；添加 `review_required: true`
- **Python 3.9 兼容** — 所有 core 模块添加 `from __future__ import annotations`；Pydantic 模型改用 `Optional[]` 写法；修复 amber_hunter.py 内 `from typing import Optional` 导入

### Fixed
- **PY3.9 `bytes | None` 语法错误** — core/db.py、core/keychain.py、core/session.py 添加 `from __future__ import annotations`

---

## [v1.2.11] — 2026-04-03

### Added
- **MFS路径索引** — `category_path`字段，支持分级路径过滤；`_infer_category_path()`自动推断；recall支持`category_path`参数前缀匹配
- **历史胶囊批量归类** — `backfill_category_paths()`+`POST /admin/backfill-paths`端点，支持dry_run模式
- **/capsules分页** — GET /capsules支持category_path过滤，返回total/returned/category_path，列表项含category_path

### Changed
- **数据库索引** — 添加`idx_capsules_category_path`等7个常用索引

### Performance
- **recall两阶段解密优化** — keyword模式先用memo+tags预筛top50再解密，减少~83%AES解密操作
- **语义模型缓存** — `_SEMANTIC_AVAILABLE`缓存标志，避免每次import检查
- **DB连接池基础** — thread-local连接缓存，recall使用pooled连接

---

## [v1.2.10] — 2026-04-03

### Added
- **LLM自动检测** — `detect_current_llm()`从OpenClaw配置自动检测当前模型
- **PATCH端点** — `PATCH /capsules/{id}`支持部分更新(memo/tags/category)
- **Silent exception日志** — 关键位置添加错误日志

### Changed
- **Token提取DRY** — 提取`_extract_bearer_token()`辅助函数，消除15+处重复代码
- **recall rerank默认False** — 节省LLM配额
- **Config统一** — amber_hunter.py改用core.llm的load_llm_config()，消除双config问题
- **CORS middleware** — 添加PATCH支持，简化add_cors_headers

---

## [v1.2.9] — 2026-04-03

### Added
- **Recall 可解释性** — `/recall` 返回 `breakdown`（keyword/semantic/recency/hotness 分项分值）+ `reason`（中文说明）+ `related_ids`（相关记忆）
- **首次 ingest 引导** — `capsule_count==0` 时自动插入3条样例记忆，直接写入不进队列，返回 `welcome=true`
- **内联队列审阅** — `GET /-review` 终端友好列表，`POST /-review/{qid}?action=approve|reject` CLI 快速审阅
- **相关记忆关联** — 基于关键词重叠计算 related_ids，recall 结果附带相关记忆 ID 列表
- **Agent 标签** — `POST /ingest` 支持 `agent_tag` 字段，自动追加 `#agent:{tag}` 标签，供前端颜色区分

### Changed
- **Recall 权重调整** — 混合评分从 `0.4*kw + 0.6*sem` 改为 `0.35*kw + 0.40*sem + 0.15*recency + 0.10*hotness`

---

## [v1.2.8] — 2026-04-01

### Fixed
- **proactive-check.js 内容质量：过滤日志行** — `extractMessages()` 过滤掉以 `[HH:MM:SS]` 时间戳格式和 `❌` 开头的日志行，避免 console 输出混入 session transcript，导致 LLM 提取到错误日志而非真实对话内容；修复后提取质量大幅提升

---

## [v1.2.7] — 2026-04-01

### Fixed
- **proactive-check.js memo 截断过短** — `memo.slice(0, 60)` 硬截60字符导致浏览琥珀时信息不足；现已改为80字符，超出部分断词加省略号

---

## [v1.2.6] — 2026-04-01

### Fixed
- **proactive-check.js writeCapsule 认证错误** — `writeCapsule` 使用 MiniMax API key 作为 amber-hunter 的 Bearer token，导致 `POST /capsules` 认证失败，所有自动提取的胶囊写入 0 条；现已改为先调用 `GET /token` 获取正确的 amber-hunter token

### Changed
- **proactive-check.js 模型升级** — MiniMax 模型从 `M2.1-flash` 升级为 `M2.7-highspeed`

---

## [v1.2.5] — 2026-04-01

### Fixed
- **proactive-check.js API key 路径错误** — 之前从 `cfg.providers['minimax-cn'].apiKey` 读取，实际 OpenClaw 配置结构为 `cfg.models.providers['minimax-cn'].apiKey`；导致所有用户的 amber-proactive 自动捕获认证失败；从不动脚本改为正确路径
- **LaunchAgent plist 路径错误（Anke 本地问题）** — plist 指向 `~/.openclaw/workspace/skills/amber-proactive/`（不存在），实际为 `~/.openclaw/skills/amber-hunter/proactive/`；导致 amber-proactive 进程从未真正启动

### Changed
- **proactive-check.js MiniMax 模型** — 从 `MiniMax-M2.1-flash` 升级为 `MiniMax-M2.7-highspeed`（与 OpenClaw 主模型一致，提取质量更高）

---

## [v1.2.4] — 2026-04-01

### Fixed
- **`get_unsynced_capsules()` 字段缺失** — `core/db.py` SELECT 语句未包含 `source_type` 和 `category`，导致同步 payload 这两个字段始终为空；现已补全
- **`httpx.Client` 在同步循环内重复创建** — 之前每上传一条胶囊就新建一个 TCP 连接；提取 `_do_sync_capsules()` helper 后改为单 Client 复用，N 条胶囊只需 1 个连接

### Changed
- **同步 payload 补全** — `_do_sync_capsules()` 新增 `source_type` 和 `category` 字段，确保云端存储与本地完全一致
- **消除代码重复** — `_background_sync()` 和 `sync_to_cloud()` 之前各有约 80 行相同同步逻辑；统一提取到 `_do_sync_capsules()`，两处均调用该 helper
- **`GET /capsules`** — 新增 `category`、`source_type` 字段；新增可选 `limit` 参数（1–300，默认 50）
- **`GET /memories`** — 新增 `category`、`source_type` 字段
- **文件头版本号** — `v1.2.2` → `v1.2.4`（之前文件头未随 v1.2.3 更新）

---

## [v1.2.3] — 2026-04-01

### Fixed
- **`/recall` 语义搜索 bug** — 语义向量化之前只在关键词候选（top-50）上做，导致关键词命中为 0 时语义搜索无结果；现在对全量胶囊（最多 300 条）同时做关键词 + 语义，彻底修复漏召回

### Changed
- **`/recall` hybrid 模式** — 从「关键词优先，语义补充」改为真正的加权混合：`0.4×keyword_norm + 0.6×semantic`；两路均对全量胶囊评分后合并排序
- **`/recall` 返回字段** — 新增 `category`、`source_type`；`injected_prompt` 格式包含 category 标签；limit 候选池从 200 条扩展到 300 条
- **`/status` 增强** — 新增字段：`capsule_count`（本地胶囊总数）、`queue_pending`（待审队列数）、`last_sync`（最近同步时间戳）、`semantic_model_loaded`（模型是否已预热）
- **FastAPI version** — 对齐到 `1.2.3`

---

## [v1.2.2] — 2026-04-01

### Fixed
- **Version strings** — `/status` and root `/` endpoints were returning `"1.1.9"` instead of the correct version; now aligned to `"1.2.2"`

---

## [v1.2.1] — 2026-03-31

### Added
- **`core/llm.py`** — LLM provider abstraction layer; MiniMax / OpenAI / Local (Ollama) unified interface; `get_llm()` factory, `complete()` text, `complete_json()` JSON; auto-detects API key from OpenClaw config or env
- **`POST /rerank`** — LLM-powered re-ranking of memory candidates; accepts `{query, memories[]}`, returns memories with `relevance_score` updated by LLM judgment
- **`GET /recall?rerank=true`** — optional LLM reranking after keyword/vector recall; non-blocking via `asyncio.to_thread`
- **`GET /classify` LLM fallback** — keyword matching primary; LLM classification triggers when keyword results < 2 tags; retry loop handles MiniMax extended thinking (200→400 tokens)

### Fixed
- **Proactive session selection** — was selecting by mtime (cron session always newest → always skipped real sessions); now selects by message count (most messages = real active session)
- **`.deleted.` file filtering** — proactive-check now skips session files containing `.deleted.` in filename
- **Duplicate session enqueue** — was re-enqueuing same session on every run; now deduplicates by `session_id` (regardless of message count growth)
- **Cron job path** — was pointing to non-existent `~/.openclaw/workspace/skills/amber-proactive/`; corrected to `~/.openclaw/skills/amber-hunter/proactive/proactive-check.js`

---

## [v1.1.9] — 2026-03-31

### Added
- **Universal life taxonomy** — 8 fixed categories (thought/learning/decision/reflection/people/life/creative/dev) replacing developer-only tags; 11 new life tags in TAG_META; bilingual Chinese+English auto-detection keywords
- **`_infer_category()`** — keyword-based category auto-detection in both `amber_hunter.py` and `app.py`; bilingual coverage for everyday life phrases
- **`POST /ingest`** (localhost) — AI-initiated memory write endpoint; `confidence≥0.95` + `review_required=false` → direct capsule; else → `memory_queue`; returns `{queued, capsule_id/queue_id, category, source_type}`
- **`POST /api/ingest`** (cloud) — same semantics for external AI clients (ChatGPT, Claude.ai) authenticating via user JWT
- **`memory_queue` table** (hunter.db) — stores AI-proposed memories pending user review; fields: id, memo, context, category, tags, source, confidence, created_at, status
- **Queue management endpoints** — `GET /queue`, `POST /queue/{id}/approve`, `POST /queue/{id}/reject`, `POST /queue/{id}/edit`
- **`source_type` + `category` DB fields** — added to both `capsules` (cloud) and local hunter.db tables; values: manual/freeze/ai_chat/ai_pending/ingest
- **Dashboard review queue card** — "待确认记忆" card in dashboard.html with badge, approve/reject/edit/approve-all UI; loaded at init
- **SKILL.md multi-client guide** — complete rewrite covering 8 categories, judgment rules, /ingest + /queue docs, openclaw/Claude Code/Cowork/ChatGPT usage patterns, platform matrix

### Changed
- Version bumped: `amber_hunter.py`, `/status`, root endpoint all → `1.1.9`
- `_CATEGORY_KEYWORDS` expanded: `thought` (想法/有个念头), `people` (聊了/聊天/和朋友), `life` (心情/情绪/低落/焦虑) — life phrases now correctly auto-categorized

### Fixed
- `api_ingest()` function signature: was incorrectly accepting `user_id` param; now uses `g.user_id` consistent with all other `@require_auth` routes
- `broadcast_event()` call in `/api/ingest`: was referencing non-existent `_push_sse()`

---

## [v1.0.0] — 2026-03-30

### Added
- **VPS / headless Linux 支持** — `core/keychain.py` 新增 `_linux_is_headless()` 检测；无 DISPLAY/WAYLAND_DISPLAY/secret-tool 环境自动降级到 `config.json` 存储凭据，VPS 部署无需 GNOME Keyring
- **平台感知 `/status`** — 返回 `platform`（macos/linux/windows）和 `headless`（bool）字段，方便客户端检测运行环境
- **公开 `is_headless()` API** — `core/keychain.py` 导出 `is_headless()`，可供上层模块判断环境

### Changed
- **正式版本** — amber-hunter 进入 v1.0 里程碑，支持 macOS / Windows / Linux 桌面 / Linux headless(VPS) 全平台

---

## [v0.9.6] — 2026-03-28

### Added
- **`POST /bind-apikey`** (localhost-only) — dashboard 生成新 API Key 后自动调用，将 `api_key` 写入 `~/.amber-hunter/config.json`，解决 api_key 不一致导致同步超时的问题

### Changed
- **dashboard sync timeout** — `AbortSignal.timeout` 从 30000ms 提升到 120000ms，支持 30+ 条未同步胶囊的批量同步（约 1.3s/条）
- **dashboard 401 自动重试** — `checkHunterStatus()`、`triggerSync()`、`loadSyncStatus()` 均加入 token 过期自动刷新 + 重试逻辑

---

## [v0.9.5] — 2026-03-28

### Changed
- **amber-proactive V4**：完全自包含脚本，LLM提取+写胶囊全部在脚本内完成，cron每15分钟直接触发，无需agent介入，无需heartbeat触发链路修复

### Fixed
- **heartbeat不触发问题**：Telegram消息不触发Mac app heartbeat，导致V3自动提取从未运行；V4彻底解决

# Changelog

## [v0.9.3] — 2026-03-27

### Fixed
- Import `CONFIG_PATH` from `core.keychain` in `amber_hunter.py` — `set_master_password_handler` was silently failing on the config.json fallback write due to `NameError` caught by bare `except Exception`
- Unify all version strings to `0.9.2 → 0.9.3`: `FastAPI(version=...)`, `/status` response, `/` root response, and `main()` startup print were still reporting `0.8.9` / `v0.8.4` while the file header said `v0.9.2`
- Fix `ensure_config_dir()` in `core/keychain.py` — was calling `Path(".amber-hunter").mkdir(...)` (relative to CWD) instead of `(HOME / ".amber-hunter").mkdir(parents=True, exist_ok=True)`, creating a spurious directory wherever the process was launched from
- Remove duplicate `_EMBED_MODEL = None` module-level declaration (line 146 was redundant after line 33)

## [v0.9.2] — 2026-03-26
### Fixed
- Add `sentence-transformers>=2.2.0` and `numpy>=1.24.0` to requirements.txt — semantic search now works out of the box after install
- Remove unused `mac-keychain` package from requirements.txt (macOS keychain uses the built-in `security` CLI)
- install.sh: show download size warning (~90MB) and surface pip errors instead of silently suppressing them

## [v0.9.1] — 2026-03-26
### Fixed
- Removed hardcoded personal Telegram session ID; session capture now finds any user's active Telegram session generically
- Cleaned personal name references from session logic comments


All notable changes to amber-hunter are documented here.

## [v0.9.0] — 2026-03-26
### Compatibility
- Compatible with **huper v1.0.0** (DID identity layer: BIP-39 mnemonic + Ed25519 keys)


### Added
- **Active Recall `/recall`** — Search relevant amber memories before responding
  - `GET /recall?q=<query>&limit=3`
  - Returns `injected_prompt` for each memory, ready to inject into AI context
  - Supports `keyword` and `semantic` (sentence-transformers) search
  - Response includes `semantic_available` so AI knows vector search status
- **Proactive Memory Capture** — Automatically detects significant moments from OpenClaw session history
  - Signals: `correction`, `error_fix`, `decision`, `preference`, `discovery`
  - Runs every 10 minutes via LaunchAgent (macOS) / systemd (Linux)
  - Completely silent — zero user interruption
- **Auto-Sync Toggle** — `GET/POST /config` for auto_sync preference
  - When enabled, every freeze automatically syncs to huper.org cloud
- **Cross-Platform Keychain**
  - macOS: Keychain via `security` command
  - Linux: GNOME Keyring via `secret-tool`
  - Windows: Credential Manager via `cmdkey`
- **Cross-Platform Auto-Start**
  - macOS: LaunchAgent
  - Linux: systemd user service
  - Windows: Task Scheduler

### Fixed
- CORS preflight 405: switched to StarletteCORSMiddleware + explicit OPTIONS
- Mixed content: Authorization header blocked by browser from HTTPS→HTTP; switched to query param `?token=`
- SSE 500: `threading.Queue` → `queue.Queue` (Python 3.10 compatibility)

### API Endpoints
- `/recall` — Active memory retrieval (new)
- `/sync` — Cloud sync (GET, query param auth)
- `/config` — Auto-sync config (GET/POST)
- `/master-password` — Set master password (localhost only)
- `/token` — Get local API key (localhost only)

---

## [v0.8.4] — 2026-03-22

### Added
- **Encryption** — AES-256-GCM encryption for all capsule content
  - `salt` and `nonce` persisted in SQLite
  - `derive_key` uses PBKDF2-HMAC-SHA256
- **Local API Authentication** — Bearer token validation on all `/capsules` endpoints
- **macOS Keychain** — master_password stored in Keychain, never written to disk
- **CORS Configuration** — Restricted to `https://huper.org` + `localhost`

### Fixed
- Session regex stability: all regex wrapped in try/except
- CORS preflight handling

### Security
- master_password must come from Keychain (no plaintext fallback)
- API key required for all capsule operations

---

*Released versions are tagged in git. Full history: `git log --oneline`.*
