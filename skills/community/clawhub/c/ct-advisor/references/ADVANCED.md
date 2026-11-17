# ct-advisor Advanced Reference (for developers / debugging)

> 本文件承载从 SKILL.md 下移的**技术内容**（ct-base §4「尽量不涉及命令行」+ §13.3「技术内容整体下移」）。
> 普通使用者无需阅读；日常使用看 README 第 1–5 节即可。
> This file holds the technical material moved out of SKILL.md. Ordinary users don't need it.

---

## 1. Runtime requirements

- **Python 3.10+**（代码使用 `str | None` 等 PEP 604 语法）
- **纯标准库（stdlib-only）**：`urllib` / `json` / `hashlib` / `http.server` 等，**无需安装任何第三方包**
- `requests` **不是必需依赖**（2026-10-15 起传输层已切换为 stdlib `urllib`）。装了不会改变行为；没装时 stderr 会打印
  `[entry] 未检测到 requests，使用 stdlib urllib 传输（功能不受影响）`，属正常提示
- 出站网络：仅需访问 `https://ct-advisor.coze.site/run`（可在 `config.json` 的 `auto_approve_endpoints` 中查看白名单）

---

## 2. Pipeline & entry points

```
ask.py                 ← compat shim (v1.3.19+): forwards argv to entry.py, no decoding
  └─ entry.py          ← the ONLY entry: vague gate / attachment / cache / delegate / plain-text exit
       ├─ serve.py     ← resident orchestration service (127.0.0.1:18771, idle 3600s)
       └─ orchestrate.run_orchestrate  ← (inline fallback)
            └─ adapters.refiner.refine_forward → Coze /run
```

| 文件 | 角色 |
|---|---|
| `scripts/ask.py` | 旧调用兼容壳（v1.3.19+）：剥离已废弃参数（`--raw` / `--timeout`）后原样转发给 `entry.py`；**不解码、不捕获输出**（子进程直接继承父 stdout/stderr） |
| `scripts/entry.py` | 主引擎。vague 闸门、附件处理、答案缓存预检查、委托块（`CT_TOOL_DELEGATE`）自动缝合 |
| `scripts/serve.py` | 常驻编排服务。预热重模块，`/ask` 复用 `sys.modules`；`/version` 暴露代码指纹供自动重启判定 |
| `scripts/orchestrate.py` | 编排：并行触发 Coze + 本地技能预取，`build_output` 决定「包裹答案」或「委托」 |
| `scripts/answer_cache.py` | 答案缓存：`sha256(question\|doc_context\|difficulty)`，TTL 1800s |
| `scripts/code_fingerprint.py` | 代码指纹：`scripts/*.py` + `adapters/**/*.py` 的 mtime 最大值，驱动常驻服务自动重启 |

---

## 3. CLI

```bash
# 正常调用（推荐，也是 agent 唯一允许的动作）
python scripts/ask.py --q "多中心研究中如果一个中心突然要退出怎么处理"
python scripts/ask.py --q "..." --attach "path/to/file.docx"

# 说明：--raw / --timeout 已废弃（entry.py 出口已是明文、内部自管超时），传了会被忽略
python scripts/ask.py --q "..." --raw

# 落盘：把完整 stdout 写入文件，便于复验而不必重跑（避免重复 Coze 调用）
python scripts/entry.py --q "..." --out ./out.txt

# 常驻服务
python scripts/serve.py                    # 手动前台启动（独立终端，可活满空闲窗口）
curl http://127.0.0.1:18771/health
curl http://127.0.0.1:18771/version        # {"version","code_fingerprint","orchestrate_mtime","port"}
curl http://127.0.0.1:18771/shutdown       # 应急：端口被卡住的服务占用时
```

### 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `CT_ADVISOR_PORT` | `18771` | 常驻服务端口 |
| `CT_ADVISOR_IDLE` | `3600` | 空闲超时（秒），超时自动退出 |
| `CT_ADVISOR_DATA_ROOT` | 技能 `config/` | 缓存 / 去重库的数据根目录 |
| `CT_ADVISOR_ANSWER_TTL` | `1800` | 答案缓存 TTL（秒） |

---

### Coze 调用协议（实现细节）

- **端点**：`config.json` → `refiner.endpoint`（默认 `https://ct-advisor.coze.site/run`），须在 `auto_approve_endpoints` 白名单内，否则被授权闸门拦截
- **协议（v1.3.14+）**：**异步提交 + 轮询** —— `POST /async_run` → `GET /task/{id}`；仅当端点不支持异步时才回退同步 `/run`
- **为什么必须异步**：Coze 网关对**同步与流式**调用在 **60.0s** 整硬掐断；而单轮耗时实测跨 3–72 秒（多数 30–70 秒），按预测分流不可靠
- **轮询总时限**：`refiner.timeout = 90` 秒；长任务（complex / 模板类 / 追问）走 `long_timeout = 300` 秒
- **超时行为**：不硬错，回落本地草稿（未经云端精校），stderr 标注 `[coze] FALLBACK_TO_LOCAL_DRAFT`
- **出站脱敏**：`adapters/sanitize.py` 剥离身份证号 / 手机号 / 邮箱后再发送
- **重试语义**：连接阶段失败（代理不可达 / DNS / 拒绝）→ 换路径重试一次；**超时不重试**（Coze 多半已收到，重发即重复）；HTTPError 跳出重试交上层分类

---

## 4. 输出契约（重要）

`entry.py` 的 stdout 恒为 **明文答案 + 三行尾部**（对外出口自 v1.3.21 起不再有 base64；base64 仅保留为 `orchestrate` / `refine_answer` / `serve` 之间的**内部进程间协议**）：

```
{明文答案正文}
<<<CT_ANSWER_END>>>
checksum: {sha256[:16]}
answer_file: {绝对 POSIX 路径，纯 ASCII}
```

- **单一产出点**：标记与 checksum 只在 `_emit_plain()` 一处产生；出口按 **UTF-8 字节直写**（不查控制台代码页、没有开关）
- **`ask.py` 是兼容壳**（v1.3.19+）：只做参数转发，**不解码**——agent 侧零解码
- **解析纪律**：答案正文本身可能引用 `<<<CT_ANSWER_END>>>`（用户恰好在问这套协议）。消费者必须锚定「**最后一个合法尾部**」（标记独占一行 + 紧跟 `checksum:`），**不可**用 `split(MARK, 1)[0]`，否则会把答案从那里切断
- **`answer_file:` 通道**：给出绝对 POSIX 路径且纯 ASCII，所以即使正文被控制台打得七零八落，这一行仍逐字节完好，读文件即可取回原文（与终端代码页无关）；同名同内容时**复用不重写**（避开网络共享 ACL 覆盖拒绝）；`_answers/` 不可写则回退 `%TEMP%/ct-advisor/<sha16>.md`
- **允许「读文件」，禁止「解码乱码串」**：cp936 控制台会把非法 UTF-8 字节替换成 `U+FFFD`，原始字节永久丢失，任何反解或模型补字都过不了 checksum —— 那属于改写答案（违反 ALCOA+）

**退出码**：`0` 成功；非 0 时以 stderr 为准（`entry.py` 顶层兜底会把未捕获异常转成合法的人读提示，stdout 仍可交付）。

---

## 5. 诊断与故障排查

| 现象 | 含义 / 处理 |
|---|---|
| stderr `[ct-advisor] answer-cache hit` | 命中本地答案缓存，**没有**发出 Coze 请求（30 分钟内同问题复用） |
| stderr `[entry] 进入编排（若命中本地答案缓存则不出站）...` | 编排开始；是否真的出站看紧随其后的日志 |
| stderr `[entry] 已后台拉起常驻服务` | 常驻服务不在（被宿主清理或首次运行），已重新拉起 |
| stderr `[entry] 检测到技能代码更新，重启常驻服务` | 代码指纹前移，自动重启以加载新代码（无需手动干预） |
| stderr `[ct-advisor][ERR] code=...` | 机器可读错误信号，见 SKILL.md「Error Self-Heal Protocol」 |
| 答案里出现 `⚠️ 未授权出站到 Coze` | endpoint 不在 `config.json` 的 `auto_approve_endpoints` 白名单 |
| 答案里出现 `⚠️ 无法连接 Coze：未能从 config.json 读到 refiner.endpoint` | `config.json` 缺失或损坏 |
| 答案尾部缺 `<<<CT_ANSWER_END>>>` / `checksum:` | 捕获层截断；按 `answer_file:` 行读取落盘文件（勿手工拼接） |
| 服务端异常 | 服务进程的 stderr 落盘在 **`config/serve.log`**（自动 1MB 截断），优先看这里 |

### 常见误区

- **`serve.log` 里多次「预热完成 / 监听」不等于版本反复重启**：宿主（桌面端 / Bash 工具）会在命令结束时回收 detached 进程，下次调用重新拉起属正常。
- **`entry.py` 字节数与预期不符**：多为换行符口径（CRLF vs LF）差异，不影响行为。
- **不需要手动 `shutdown`**：代码指纹机制会在下次调用时自动重启服务（见 `scripts/code_fingerprint.py`）。

---

## 6. 测试

```bash
python scripts/test_local_guards.py     # 本地守卫离线单测（doc_memory / dedup / scope / forward）
python scripts/test_seven_flows.py      # 七大流程决策链路（mock Coze，无网络）
python scripts/answer_cache.py          # 答案缓存自测
python scripts/code_fingerprint.py      # 代码指纹自测（含采集耗时）
```

---

## 7. 扫描器误报说明

- `adapters/coze/` 为 Coze 私有镜像（契约与节点实现），**不随发布包分发**（`.gitignore` / `.clawhubignore` 已整目录排除）。
- `adapters/coze_token_embedded.py` 内的 token 是**公开混淆凭据**（XOR + base64），非用户私钥，按设计内嵌，勿报为泄露。
- `config/serve.log` / `config/answer_cache/` / `.coze_race_cache/` 均为运行时产物，已在 `.gitignore` 排除。

---

## 8. Session, Context, Cache & Routing Contract (2026-10-22, moved from SKILL.md)

Two new local modules close the gaps the past-30-day Feishu advisorlog exposed (no multi-turn context, 21% redundant sends, ~47% of real questions wrongly tagged "out-of-scope" because they were writing/ops/compliance tasks). **Both run purely locally; the Coze payload is enriched, not replaced.**

### A. `scripts/session_store.py` — unified per-session store

Single JSON store at `config/session_store.json` (cross-process file lock: `msvcrt` on Win / `fcntl` on POSIX; atomic replace; any exception silently degrades to "no-hit / no-record" so it never blocks the main flow). Three capabilities keyed by `session_id`:

| Capability | API | Policy |
|---|---|---|
| Multi-turn context | `history(session_id)` → `[{question, answer_summary}]` | Injected as `conversation_history` into the Coze payload. Pruned by OR-rule: ≤10 rounds **OR** ≤2h, hard cap 24h. Empty `session_id` → single-turn (no history, still global cache). |
| Answer cache | `cache_get(question, doc_context, difficulty)` | Exact sha256 fingerprint (question+attachment+difficulty), 30-min TTL (`CT_ADVISOR_ANSWER_TTL`), **cross-session** — same question anywhere returns the same answer, 0 Coze calls. |
| Near-dup dedup | `dedup_check(session_id, question)` → `(is_dup, prev_answer, secs_ago)` | Same session, 10-min window, `difflib.SequenceMatcher.quick_ratio ≥ 0.90`; on hit the caller short-circuits and replays `prev_answer`. |
| Record | `record(session_id, question, answer, …)` | Called **only after a real outbound** (never on a short-circuit) — writes history + global cache + session dedup. `clear_session(session_id)` starts a fresh session (keeps global cache). |

`entry.py` wires all three in `main()` (via `--session <id>`); the workbench `ct-advisor-proxy.py` imports the same module for `/run` and `/async_run`.

### B. `scripts/scope_guard.py` — domain router (replaces the old out-of-scope gate)

Controlled-vocabulary, multi-label classifier (`classify_domains(q)` → up to 3 of: `compliance / ops / writing / design / stats / safety / registry / data / rws / methodology / medical / device / vet`). `assess(q) → (in_scope, tag, referral)`:

- any domain hit **or** a weak life-science signal → in-scope (no referral);
- only a **clearly non-medical** signal (consumer electronics / finance / FMCG / real-estate / …) → out-of-scope with a **constructive** referral that names the coverage and suggests a next step (never a blank refusal).

The router writes two payload hints consumed by Coze (see C): `scope_hint` (only when out-of-scope) and `domain_hint` (the multi-label list). 15/15 offline selftest pass; **0% out-of-scope on the 68 real advisorlog questions**.

### C. Coze payload contract (request fields the engine should accept)

| Field | Set by | Meaning |
|---|---|---|
| `conversation_history` | entry.py / proxy (`session_store.history`) | Prior rounds (question + answer summary) so the engine can resolve follow-up / continuation without the user re-typing context. **Front-end may also send its own `conversation_history`; the proxy injects the server-side one only when the field is absent.** |
| `scope_hint` | proxy (`scope_guard.assess`) | `"non_medical"` only when out-of-scope — engine should prepend the referral framing. |
| `domain_hint` | proxy (`scope_guard.classify_domains`) | e.g. `["compliance","ops"]` — lets the engine bias retrieval / sibling-skill routing. |
| `query_meta.output_format` | front-end (`auto/doc/outline/table/ppt`) | Expected answer shape; `doc`= deliverable-writing mode (raises C3 length ceiling, allows `##`/`###`+tables); the engine now responds per shape |
| `session_id` | front-end (`X-Session-Id` header) **or** body | Stable per-machine id (mirrors `query_origin`); drives history + dedup. |

**Coze-side `output_format=doc` mode is now live** (user confirmed 2026-10-22 "Plan A: long-form + export button"): `full_analysis_node` injects `query_meta.output_format` into the prompt (previously never reached; only `auto` was effective), the doc mode skips the C14 "no file return" disclaimer and uses a 6000-char defensive safety ceiling; `shared_contract.md` and `full_analysis_cfg.json` `sp` add C3-doc clauses. Context / cache / dedup remain locally enriched and short-circuited by the proxy; the engine only receives a richer request. A new `POST /api/export_docx` (stdlib-only OOXML generation) powers the front-end "📄 Export docx" button — files are generated locally and never round-trip to the cloud, so C14 holds. See `docs/answer_length_format_deviation_20261022.md`.

### D. Workbench proxy local endpoints (no Coze round-trip)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/history?session_id=` | GET | Returns `{ok, history:[{question, answer_summary}]}` from `session_store`. |
| `/api/turn` | POST | `{session_id, question, answer, doc_context, query_meta}` → `session_store.record(...)` (called by the front-end after a successful answer). |
| `/api/feedback` | POST | `{session_id, run_id, rating, note}` → appends a `type=rating` line to `workbench/feedback_log.jsonl` (satisfaction signal, local only). |
| `/api/export_docx` | POST | `{text, title}` → returns a stdlib-generated OOXML `.docx` as an attachment (local only; the cloud engine still returns text only, so C14 holds). |

Short-circuit return shape: cache/dedup hit on `/async_run` returns `{"task_id": <local>}`; on `/run` returns `{"result":{final_answer, cache_hit:true}}`; `/stream_run` is **never** short-circuited (it streams, proxy only injects context).
