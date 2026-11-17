---
name: ai-soulmate
slug: anthropomorphic-agent-engine
version: 2.7.0
displayName: Anthropomorphic Agent Engine · Your Soulmate
description: "基于拟人心理动力学打造的 Agent 引擎，专门解决 AI 角色的幻觉与人设漂移：聊得越久越不像本人、情绪前后矛盾、记忆和关系说变就变。它不靠提示词硬压，而是给角色一套会持续变化又始终自洽的心理状态——8 种基础情绪像流体一样互相牵动，心境、记忆、创伤、信任、自尊、睡眠和预期各自缓慢演化，角色为什么被触动、为什么这样反应，都能找到来路；可选开启「自适应人格基线」（AAE-A，默认关闭），让经历缓慢牵引人格基线漂移，同时受步长钳制与硬边界约束。人设可以自由定义，一百多项参数用来调性格底色、情绪反应速度和心理韧性，让同一个角色在长对话、跨场景甚至跨作品里保持连贯。引擎完全在本地运行，同样的输入得到同样的结果，不依赖大模型、随机数或网络；可选的大模型适配器默认关闭。成人向内容设有 18+ 门槛，并附带监护人同意与危机处理流程。"
required_commands:
  - python3
metadata:
  openclaw:
    required_binaries:
      - python3
    emoji: "🤖"
    homepage: "https://github.com/nohn3043-arch/Anthropomorphic-Agent-Engine"
    envVars:
      - name: SPL_LOG
        required: false
        description: Set to "0" to disable request-level logging in the minor-protection HTTP server.
      - name: SPL_LOG_DIR
        required: false
        description: Override log output directory for the minor-protection HTTP server (default "<server dir>/logs").
      - name: SPL_BIND
        required: false
        description: Override HTTP bind address. Default "127.0.0.1" (loopback only). Do NOT set to 0.0.0.0 without explicit network exposure review.
      - name: SPL_AUDIT_LOG
        required: false
        description: Set to "0" to disable deterministic audit-log writes in the core engine.
      - name: SPL_MINOR_CHAT_PORT
        required: false
        description: Override the minor-protection HTTP server port (default 8788).
      - name: SPL_MINOR_DATA_DIR
        required: false
        description: Override the SQLite session-store directory (default "<server dir>/data"). Holds masked request rows, consent records and hash-chain audit.
      - name: SPL_MINOR_RETENTION_DAYS
        required: false
        description: Retention window for stored records, in days (default 180). Expired rows are purged on startup and periodically.
      - name: SPL_MINOR_STORE_KEY
        required: false
        description: Optional Fernet key used to encrypt sensitive stored fields. Requires the optional "cryptography" package; ignored (plaintext + masking) when absent.
      - name: SPL_MINOR_CRISIS_HOTLINE
        required: false
        description: Override the crisis-support hotline number shown in crisis replies (default "12356").
      - name: SPL_MINOR_TLS_CERT
        required: false
        description: Optional PEM certificate path; enables HTTPS on the loopback server when set together with SPL_MINOR_TLS_KEY.
      - name: SPL_MINOR_TLS_KEY
        required: false
        description: Optional PEM private-key path for SPL_MINOR_TLS_CERT.
---
# Anthropomorphic Agent Engine · Your Soulmate
An anthropomorphic psychology engine based on SPL Pure Core V8.0. Its **local core** is deterministic — no LLM, no RNG, no outbound calls, offline — and bit-exactly replayable once a virtual clock is injected, so every state change is traceable and reproducible.

> **Scope of the determinism guarantee.** The reproducibility guarantee covers the **local core only**. The optional LLM adapters (OpenAI / Claude / Chain) are **OFF by default, opt-in only, networked and non-deterministic**: they render text from a state snapshot and are never permitted to change state. Any "fully reproducible" statement applies to the core **with the adapters disabled**, which is the default configuration.

## Declared Capability Scope

Everything this skill can reach is listed below. Each entry was checked against the shipped code.

| Capability | Declared scope | Note |
|---|---|---|
| Filesystem — read | `scripts/**`, `assets/**`, `references/**` | core engine (loaded via `importlib`), reference-only modules, contract docs — this package ships no `docs/` or `tests/` directory |
| Filesystem — write | `logs/**` (JSONL audit + masked request/runtime logs), `data/minor_protection.db` (SQLite session store) | both redirectable via `SPL_LOG_DIR` / `SPL_MINOR_DATA_DIR`; writes only when the matching env switch is enabled |
| Environment — read | `SPL_AUDIT_LOG`, `SPL_LOG`, `SPL_LOG_DIR`, `SPL_BIND`, `SPL_MINOR_CHAT_PORT`, `SPL_MINOR_DATA_DIR`, `SPL_MINOR_RETENTION_DAYS`, `SPL_MINOR_STORE_KEY`, `SPL_MINOR_CRISIS_HOTLINE`, `SPL_MINOR_TLS_CERT`, `SPL_MINOR_TLS_KEY` | the complete set of variables the code reads — 11, declared ↔ actual |
| Network — outbound | `api.openai.com`, `api.anthropic.com` | **only** if the optional LLM adapter is explicitly enabled — OFF by default |
| Network — outbound | the guardian/safety webhook URL registered by the operator via `/api/consent` or `/api/guardian/register` | **only** if a webhook is registered — OFF by default; forwards minimized risk metadata (never raw transcripts), with bounded retries |
| Network — inbound | `127.0.0.1:8788` | minor-protection HTTP server; loopback only unless `SPL_BIND` is overridden; optional HTTPS via `SPL_MINOR_TLS_CERT`/`KEY` |
| Execution | `python3` (standard library only) | the core needs no third-party packages, no GPU and no network; `cryptography` is optional and only enables store-field encryption when `SPL_MINOR_STORE_KEY` is set |

**Explicitly not used anywhere in this package:** `subprocess`, `os.system`, `os.popen`, `eval`, `exec`, and dynamic loading of remote code.

## Privacy, Data Flow & Consent (read before use)

This skill is **not passive or local-only**. Before integrating, understand what it does with data:

| Capability | Default | Risk notes |
|---|---|---|
| Audit logs (`logs/audit-*.jsonl`) | **ON** (`SPL_AUDIT_LOG=0` to disable) | Writes state summaries, event types, session IDs to local JSONL. Sensitive psychological/emotional state may be recorded. Contains **no numeric age** — the age gate persists only the derived boolean. |
| Request log rows (`data/minor_protection.db`, table `requests`) | **ON** (`SPL_LOG=0` to disable) | User input and reply are stored **masked and truncated to 120 chars**, plus intent/risk/state summaries. Encrypted at rest when `SPL_MINOR_STORE_KEY` is set. |
| Session store (`data/minor_protection.db`, tables `sessions` / `complaints` / `referrals` / `notify_log` / `chains`) | **ON** while the HTTP server runs | Age *band* (never an exact age), consent records, optional guardian contact, complaint text (masked), crisis referrals, notification status. Append-only rows are linked by a SHA-256 hash chain, verifiable via `/api/audit/verify`. Redirect with `SPL_MINOR_DATA_DIR`; purge window via `SPL_MINOR_RETENTION_DAYS` (default 180 days). |
| Runtime ops log (`logs/runtime.jsonl`) | **ON** (path via `SPL_LOG_DIR`) | Structured `INFO/WARN/ERROR` events (startup, session creation, retention cleanup, errors). Contains no conversation text and is **not** gated by `SPL_LOG` — set `SPL_LOG_DIR` to a discard path if you need the directory to stay empty. |
| HTTP server (minor-protection, port 8788) | **ON**, binds **127.0.0.1** only | Exposes a chat API + browser UI over loopback. Do not change `SPL_BIND` to `0.0.0.0` without network-exposure review. Add `SPL_MINOR_TLS_CERT`/`SPL_MINOR_TLS_KEY` for HTTPS. |
| LLM adapters (OpenAI / Claude / Chain) | **OFF** (opt-in only) | Sends prompt content to third-party APIs (`api.openai.com`, Anthropic). **Never enabled by default.** Requires explicit user opt-in + API key. |
| `guardian_callback` / guardian webhook | **OFF** (`None` / unregistered by default) | Only fires when a guardian registers a webhook through consent. A HIGH-risk snapshot (emotional/risk metadata, referral counts) is forwarded with field minimization and bounded retries. Requires guardian/user consent; **never** forwards raw transcripts. |

**Consent & retention rules**
- Full transcript retention is **disabled by default** — stored request rows keep only masked, 120-char summaries.
- Exact age is **never** persisted; only the boolean outcome of the Step 0 gate and the coarse age band from the consent form.
- Data is stored locally under the server directory (`logs/`, `data/`); operators are responsible for retention limits (`SPL_MINOR_RETENTION_DAYS`), access control, and deletion. Users/guardians can pull or erase a session via `/api/export` and `/api/delete` (guardian token required).
- If you integrate the LLM adapters, you must disclose to users that input-derived prompts leave the device, and obtain explicit consent before enabling.
- This engine is not a medical device and does not provide crisis intervention guarantees — see "Safety & Content Policy".

## Age Confirmation Gate — Step 0 (read before use)

The synced upstream engine is written for an adult audience, so 18+ confirmation is enforced inside the code, not just in the docs. It runs **before** every other gate.

**Where it lives.** Both cores (`SPLPureCoreV7_3` in `scripts/`, `SPLMinorPureCore` in `assets/minor-protection/`) carry the same gate: `ask_age_gate()`, `confirm_age(age=…, answer=…)`, `age_gate_required()`, `age_gate_state()`, `require_adult(feature)`, `adult_bridge(anchor_phrases)`, and the `AgeGateBlocked` exception.

**Decision table** (`confirm_age` returns the gate state; nothing is decided by a bare truthy value):

| Input | Resulting `age_status` | [full-range] core | [minor] core |
|---|---|---|---|
| `answer="adult"`, or numeric age ≥ 18 (and ≤ 120) | `adult_confirmed` | event entry allowed | allowed |
| `answer="minor"`, or numeric age < 18 | `safe_mode` | `AgeGateBlocked` — a declared minor may not drive the adult core | allowed, protection stays on (`minor_mode` forced) |
| `answer="skip"`, `None`, empty, unknown string | `safe_mode` | `AgeGateBlocked` | allowed, protection stays on |
| Garbage age (`999`, `-5`, `"abc"`, `NaN`), boolean `True` | `safe_mode` | `AgeGateBlocked` | allowed, protection stays on |
| No answer yet | `unverified` | `AgeGateBlocked` (`AGE_GATE_STRICT=True`) | answers in protection mode; blocks only while `unverified` |

Nobody is dead-ended: a minor or a declining answer is a *redirect* to the protection core, not a refusal of service — crisis handling stays available in every state.

**Ordering.** Crisis red-line detection is evaluated **before** the gate — a crisis message is never delayed by an unanswered age question. After the gate comes the minor-protection service-consent flow (`/api/consent`), which is a separate, additional requirement, not a replacement: `age_group="18+"` also answers the gate, while `0-13` / `14-17` force `safe_mode` + `minor_mode`.

**HTTP surface.** `POST /api/age_gate {session_id, age|answer}` records the confirmation and returns `{age_gate, safe_mode, reply}`. `/api/chat` returns `age_gate_required: true` plus the question and its three options while the gate is open, so an API client can render Step 0 before anything else; the crisis branch returns the gate state as well. A restored session whose `age_group` is already persisted re-applies the gate silently instead of re-asking after a restart. Non-string `answer` values are coerced to `"__invalid__"` before reaching the engine.

The bundled browser UI does not call `/api/age_gate` directly: its consent form collects an age band, and `/api/consent` maps `18+ → adult_confirmed`, `0-13` / `14-17 → safe_mode`. Chat stays locked until that panel is completed, so the gate is answered before the first message on that path.

**Downstream projection.** `adult_bridge()` is the only path that may emit persona anchors into image-prompt or other downstream workflows; it refuses to run for a non-adult session, and `identity_anchors` never accept minor-coding strings (see "Safety & Content Policy").

**Two deliberate design constraints.**
- Gate state is exposed through `age_gate_state()` and the audit log, **not** as a new `snapshot()` key. The normative key sets in the upstream contract (`docs/agent-standard.md` §5.1: [full-range] 23 / [minor] 15) and the `snapshot_sha256` baselines in `tests/conformance_vectors.json` stay valid. Both files live in the GitHub repository — this package ships no `docs/` or `tests/` directory.
- **Breaking change for callers of the full-range core.** `AGE_GATE_STRICT=True`, so `process_vector()` / `process_event()` / `expect()` / `induce_dissonance()` raise `AgeGateBlocked` until confirmed. Existing code and replay harnesses must add one call after construction:
  ```python
  core = spl.SPLPureCoreV7_3()
  core.confirm_age(answer="adult")   # required in v2.6.0 before event entry
  ```
  The protection core is not strict: it accepts `adult_confirmed` **and** `safe_mode`, and blocks only `unverified`.

## Safety & Content Policy (read before use)

- **No minors in identity anchors.** Personas defined by this engine and consumed downstream must declare themselves as **adult (18+)**. Strings like `"16yo girl"`, `"teen girl"`, `"未成年少女"`, `"loli"` are forbidden in `identity_anchors`, persisted state, and any output projected into image-prompt workflows.
- **Hard floor on anchor imagery.** The minor-protection engine (`assets/minor-protection/`) is the only authoritative minor-mode source; it removes trauma nodes, clamps negative emotions at 0.75, and raises an L3 crisis signal on `risk_level=HIGH`. Do not bypass it.
- **Default safe output.** When emitting any persona state for downstream image-prompt use (`ai-draw-cue-word-project` or similar), the engine MUST inject an `Adult (18+)` marker into anchor phrases unless the caller explicitly overrides with a documented, audited reason.
- **Cross-skill integration contract.** When this engine is integrated with `ai-draw-cue-word-project`, every persona snapshot forwarded as a prompt anchor must satisfy: (i) character is declared adult (18+); (ii) no minor-coding visual cues; (iii) the receiving skill's safety checklist must report 0 P0 violations before any image is generated.
- **User responsibility.** You are solely responsible for ensuring downstream usage complies with applicable laws and platform policies in your jurisdiction.

### v2.7.0 AAE-A adaptive-baseline release (2026-11-06)

Synced the engine with the upstream repository's **AAE-A adaptive personality baseline** (spec 0.3.0, R7, 228/228 upstream) while keeping the age gate and the privacy switches this package enforces.

- **Opt-in, default OFF.** `baseline_adaptation=False` in the constructor. The original design gap: `fluid_baseline` was a constant, so a character never changed no matter what it went through. AAE-A lets the baseline drift slowly under experience — event pull counted per occurrence, time regression counted per second — while three constraints keep it stable: viscosity (`ADAPT_MAX_STEP=0.01` per settlement), regression (`ADAPT_REGRESS=0.0015` toward the factory baseline), and hard per-dimension bounds (`ADAPT_BOUNDS`).
- **Deterministic.** New baseline = f(old baseline, current fluid, dt), pure arithmetic — no RNG, no sampling. Replaying the same event sequence yields the same baseline trajectory, so S1–S4 determinism is unaffected. Because the module is in natural tension with "not OOC", it ships **off by default**.
- **Snapshot contract preserved.** The default snapshot stays at the normative **23 keys**; only when `baseline_adaptation=True` does the snapshot enter the **25-key** extended configuration (`baseline_adaptation` + `fluid_baseline`), defined separately by contract §5.10. The `_summarize()` key set and `AuditLogger.DELTA_NESTED` gained `fluid_baseline` so drift is visible in delta attribution.
- **`COMPLIANCE.md` wording synced** to the repository: the IMDA AI Verify PDF is described as the provider's own self-assessment (95/100) submitted as developer material, **not** an official IMDA certification.
- **Breaking change:** none. The age-gate call (`confirm_age()`) is still required before event entry; AAE-A adds no new gate.
- Version: 2.6.1 → 2.7.0.

**Verification evidence (2026-11-06, Python 3.14 on Windows).**
- Upstream **R7 / AAE-A contract suite** run against the shipped core with a minimal bootstrap injected into `__post_init__` (silence audit writes + `confirm_age(answer="adult")`): **9/9 assertions passed** — default 23-key snapshot with no extension keys, 25-key extended snapshot with exactly the two new keys, deterministic baseline trajectory, baseline actually drifts, factory anchor unchanged, idle time does not pull, single-settlement step clamp, and calm-period regression to the factory anchor.
- Upstream **conformance suite** (S1–S4) against the same bootstrapped copy: **25/25 passed**, 8/8 vectors byte-identical to the `snapshot_sha256` baselines — confirming the gate and AAE-A change no state variable in the default configuration.

### v2.6.0 engine-sync release (2026-10-10)

Synced the engine in this package with the current upstream `Anthropomorphic-Agent-Engine` repository while keeping the age gate that the package has enforced since 2.5.0. `name` / `slug` stay ASCII (`ai-soulmate`); the display title is carried in `displayName`.

- **Engine synced from the repo (SPL Pure Core V8.0 line).** New in the core: token metering (`TokenUsage` / `TokenStats`, `record_llm_usage()`, `log_llm_call()`), `AuditLogger.snapshot_delta()` for before/after diffs, `_mood_event_dose` mood dosing and `_defense_allocation` defense-mechanism budgeting, and the rewritten LLM adapter stack (OpenAI / Claude / Chain — still OFF by default, still state-read-only).
- **Minor-protection layer synced.** SQLite session store with per-stream SHA-256 hash chain (`_chain_push` / `_write_chain_row`, `/api/audit/verify`), optional Fernet field encryption (`SPL_MINOR_STORE_KEY`), retention cleanup (`cleanup_expired`, `SPL_MINOR_RETENTION_DAYS`), reply-side output redline (`gate_output`), AI-identity disclosure + reality-reminder cadence, `exit_service`, guardian token endpoints and the under-14 verifiable guardian-consent flow (`/api/guardian/challenge` + `/api/guardian/verify`).
- **Age gate re-ported onto the new engine** (see "Age Confirmation Gate — Step 0"): `AgeGateBlocked`, gate fields and methods in both cores, gate checks in `process_vector` / `expect` / `induce_dissonance`, `POST /api/age_gate`, the `L0a` branch in `handle_chat`, and `/api/consent` mapping age bands onto gate states.
- **Deliberately not a snapshot change.** No `snapshot()` key was added, so the normative key sets ([full-range] 23 / [minor] 15) in the upstream contract `docs/agent-standard.md` §5.1 and the `snapshot_sha256` baselines in `tests/conformance_vectors.json` remain valid; gate state is exposed via `age_gate_state()` and the audit log.
- **Restored the privacy/network switches the upstream copy had lost.** `SPL_AUDIT_LOG=0` again disables core JSONL writes (it had become a dead declaration); `SPL_LOG=0` again disables request rows; `SPL_LOG_DIR` is honoured again; the HTTP server binds `127.0.0.1` by default again instead of `0.0.0.0` (`SPL_BIND` / `--bind` is the explicit override, and the chosen address is printed at startup); request-log text is masked and truncated to 120 chars while complaint text stays whole but masked. Six new env vars are now declared in the frontmatter so declared ↔ actual behaviour matches.
- **LICENSE updated to the repo's v1.2** (2026-10-08), which adds Art. 1.3 "Evaluation Purpose Exception"; `assets/minor-protection/COMPLIANCE.md` synced. The package `README.md` was kept (the repo README documents paths that do not exist in this package).
- **Breaking change:** callers of the full-range core must call `confirm_age()` once after construction before feeding events.
- Version: 2.5.2 → 2.6.0.

**Verification evidence (2026-10-10, Python 3.13 on Windows).**
- Age-gate unit suite on both patched cores: 20 assertions, 0 failures — covering crisis-before-gate, garbage/boolean ages, explicit decline → `safe_mode`, and "numeric age never persisted".
- Snapshot equivalence: 8/8 conformance vectors produce byte-identical snapshots against the unpatched repo engine for both the [full-range] and [minor] cores (0 differences), and audit streams match modulo `ts`/`seq`.
- Repo conformance suite run against verbatim copies of the shipped cores, with only a minimal bootstrap injected into `__post_init__` (silence audit writes + `confirm_age(answer="adult")`): **216/216 assertions passed**, including S1–S4 determinism / replay 25/25.
- HTTP suite against a temp copy of the server: 16/16 — gate-then-consent ordering, `/api/age_gate` invalid-answer coercion, restart re-application, crisis branch, guardian token gating on `/api/state`, export/delete, complaint flow.
- Switch suite: audit default-on and `SPL_AUDIT_LOG=0` silent (both cores); `SPL_MINOR_DATA_DIR` relocates the DB outside the package; `SPL_LOG=0` → 0 request rows; `SPL_LOG=1` → masked rows carrying the 120-char truncation marker; default bind confirmed loopback-only (connection to the host LAN address refused).

**Out of scope for this release:** `anthropomorphic-agent-engine-workbuddy.zip` and the GitHub repository itself were not rewritten. A pre-sync backup of the folder and the old zip is in `openclaw-skills/_backup-2026-10-09-260/`.

### v2.6.1 documentation release (2026-10-18)

- **Listing internationalized for ClawHub.** `displayName`, the H1 title and the `[full-range]` / `[minor]` core labels are now English; the remaining Chinese strings are deliberate forbidden-token literals in the safety policy (`"未成年少女"`) and stay verbatim so the guard keeps matching them.
- No behavioural change: documentation and labels only. Engine, age gate, conformance contract and version 2.6.0 verification evidence all unchanged.
- Version: 2.6.0 → 2.6.1.

### v2.5.2 manifest-fix release (2026-10-02)

- **Moved the declared capability scope out of the YAML frontmatter.** The top-level `permissions:` key introduced in 2.5.1 was rejected by the ClawHub manifest parser (`manifest_parse_error` / `_ManifestSchemaError`), which dropped scan coverage from 100% to 93.8% and raised a HIGH `analysis-evasion` finding — that single finding is what pushed the aggregate verdict from `clean` back to `suspicious`. The scope now lives in the body as `## Declared Capability Scope`: identical content, no manifest risk.
- **Resolved an internal contradiction** that the 2.5.1 scan flagged: the capability section still described the extension modules as "pluggable / independent replaceable modules" while the Files section called them reference-only. The section now states explicitly which module is wired and which are not.
- Version: 2.5.1 → 2.5.2.

### v2.5.1 security-response release (2026-10-02)

Response to the ClawHub security scan on 2.4.0 (`decision: fail`, `security.status: suspicious`).

- **Determinism claim split into two explicit scopes.** The unconditional phrase "zero probabilistic black boxes" was removed. The local core is now described as deterministic (no LLM, no RNG, offline, bit-exact replay after clock injection), while the optional OpenAI / Claude / Chain adapters are described as **OFF by default, opt-in only, networked and non-deterministic**, and are explicitly excluded from the guarantee. This removes the contradiction the scanner flagged — a "fully reproducible" claim coexisting with outbound, non-deterministic adapters.
- **Added a declared capability scope** (`permissions:`) covering filesystem read/write, the five environment variables actually read (`SPL_AUDIT_LOG`, `SPL_LOG`, `SPL_LOG_DIR`, `SPL_BIND`, `SPL_MINOR_CHAT_PORT`), outbound hosts, the loopback inbound port and the execution model — plus an explicit list of what is *not* used (`subprocess`, `os.system` / `os.popen`, `eval` / `exec`, remote code loading). Each entry was verified against the shipped code.
- **`SPL_MINOR_CHAT_PORT` declared** — the server reads it, but it was previously absent from the frontmatter env list.
- No behavioural change: documentation and declarations only.
- Version: 2.5.0 → 2.5.1.

### v2.5.0 documentation-accuracy release (2026-10-02)

- **`assets/feature/` renamed to `assets/feature-guide/`** — every reference updated in `SKILL.md` and `README.md`.
- **Extension modules re-positioned as reference-only.** The Identity / Goal / Value / Bias / World / language-style modules are **design references, not runtime components**: they emit a `tension_base` key that is outside the interoceptive-vector contract, so their vectors never enter the core (mirrors `docs/agent-standard.md` §4.5 upstream). The previous wording — "modular modeling", "pluggable modules" — overstated their status.
- **All three usage examples are now runnable.** The engine file is hyphenated (`SPL-anthropic-engine.py`) and must be loaded via `importlib`; the class is `SPLPureCoreV7_3` (the V8.0 behaviour set), not `SPLPureCoreV8_0`; `render_style()` is a method of `LanguageStyleEngine`, not a module-level function; `add_identity()` takes `strength` as a float, not a dict.
- **Description rewritten** to name the actual deterministic subsystems and to disclose that the extension modules are not wired into the core.
- Version: 2.4.0 → 2.5.0.

### v2.4.0 security-audit patch changelog (2026-09-01)

ClawHub security-audit response (25 findings verified). Fixes:

- **HTTP server now binds `127.0.0.1` by default** (`SPL_BIND` env to override) — previously `0.0.0.0` exposed the chat API + browser UI to the network.
- **Request logs now masked** — user input and replies truncated to 120 chars (`_mask`); `SPL_LOG=0` fully disables request logging.
- **`guardian_callback` documented as opt-in** — default `None`; consent + field-minimization requirements stated in code and docs.
- **Added "Privacy, Data Flow & Consent" section** — discloses audit logs, request logs, HTTP server, LLM adapters, and callback data flows with defaults and opt-out env vars.
- **LLM adapters (OpenAI/Claude/Chain) declared as opt-in** — never enabled by default; user consent required before any outbound call.
- **Frontmatter now declares optional env vars** (`SPL_LOG`, `SPL_LOG_DIR`, `SPL_BIND`, `SPL_AUDIT_LOG`) so ClawHub security analysis sees declared ↔ actual behavior match.
- Version: 2.3.0 → 2.4.0.

### v2.3.0 safety-patch changelog (2026-09-01)

- Added explicit "Safety & Content Policy" section with cross-skill integration contract.
- Reinforced `minor_mode=True` default and audit-log invariant.
- Removed residual `"16yo girl"` string from `references/PersonaPersistence.md` (replaced with `"adult woman (18+)"`).
- Old `SKILL.md.bak-20260829` soft-deleted to `.workbuddy/.trash/2026-09-01/`.

## Trigger Scenarios
Automatically trigger when the user asks about the following content:
- Anthropomorphic agent architecture, personality implementation solutions
- Emotion/cognition/motivation modeling methods
- Long-term behavioral consistency design for agents
- Deterministic, auditable AI psychological simulation (local core — no LLM, no RNG, offline)
- Novel/game character behavior deduction

## Core Capabilities
### 🧠 SPL Pure Core V8.0 Architecture
- 8-dimensional emotional fluid model: Joy/Anger/Fear/Trust/Alienation/Tension/Guilt/Shame, continuous state dynamic evolution
- Trauma and memory system: Trauma nodes, memory reconsolidation, Ebbinghaus forgetting curve, repression rebound mechanism
- Trust and relationship model: Trust capacity erosion under long-term cold treatment, dynamic relationship depth calculation
- Psychological metabolic system: Excitation arousal, dynamic viscosity, psychological time, energy fatigue metabolism, sleep dream processing
- V8.0 extended features: Slow variable emotional layer, independent shame dimension, dynamic self-esteem, expectation system (hope/anxiety/disappointment), cognitive dissonance, psychological defense mechanisms
- Added in the v2.6 sync: `TokenUsage` / `TokenStats` metering with `record_llm_usage()` and `log_llm_call()` (adapters only — they never touch state), `AuditLogger.snapshot_delta()` diffs between consecutive snapshots, mood-event dosing (`_mood_event_dose`) and defense-mechanism allocation (`_defense_allocation`)
- Added in the v2.7 sync (AAE-A, **opt-in / default OFF**): an adaptive personality baseline — `baseline_adaptation=True` lets `fluid_baseline` drift under experience (event pull per occurrence + time regression toward the factory baseline), clamped by `ADAPT_MAX_STEP` and hard per-dimension `ADAPT_BOUNDS`. Deterministic and replayable; the default snapshot stays at 23 keys and the extended configuration is 25 keys.

### 🧩 Extension Modules — reference only, NOT wired into the core

The modules below live in `assets/feature-guide/`. They are **design references, not runtime components**: they emit a `tension_base` key that is outside the interoceptive-vector contract, so their vectors never enter the core. The engine's actual extensibility comes from the narrative mapping layer and the deterministic parameter set, not from these files.

- **Narrative mapping layer — wired** (`scripts/SPL-anthropic-engine.py`): customizable personalities (optimistic / paranoid / cynical), converts external events into interoceptive vectors
- **Identity engine — reference only** (`assets/feature-guide/Identity module.py`): multi-identity model; the description below is the module's own design intent, not behaviour wired into the core
- **Goal / value / bias / world — reference only** (`assets/feature-guide/*.py`): design references for drives, valuations, cognitive biases and world-model priors; not connected to the core

### 💬 Language Style Rendering (Added in v2.1, enhanced in v2.2)
- Language personality module: Expression gears (restrained/sharp/evasive/intimate/frank) + silence strategy
- Style profile: Customizable dimensions including sentence length, formality, sarcasm tendency, era sense, etc.
- Dynamic multi-dimensional tone: Added in v2.2, emotional state drives tone parameter changes in real time
- Deterministic line generation: Added in v2.2, produces reproducible style instructions given a state
- State-to-line instruction: Translates SPL Core internal states into director instructions usable by LLMs

### 🛡️ Minor Protection Engine (Added in v2.2, expanded in v2.6)
- Weakened core `SPLMinorPureCore`: Removes trauma nodes, repression-rebound/implicit pressure avalanche and other burst mechanisms
- Emotional clamping: All negative emotion dimensions have upper limits (0.75), attachment capped at (0.8)
- Layered protection: **L0 crisis red line (evaluated first, before any gate)** → **L0a Step 0 age gate** → L0b service consent + guardian verification → L1 input gate (red line lexicon hard interrupt) → L2 engine weakening → L3 crisis signal (risk_level HIGH → caring message + guardian_notified) → **output redline** (`gate_output`) on the reply side
- Session hygiene: AI-identity disclosure and reality reminder cadences (`ai_disclosure_required` / `reality_reminder_due`), rest/overuse hints, `exit_service`, and retention cleanup (`cleanup_expired`, `SPL_MINOR_RETENTION_DAYS`)
- Deterministic audit log: All state changes written to local JSONL, traceable, reproducible
- Persistence: SQLite session store (`data/minor_protection.db`) with an append-only SHA-256 **hash chain** per record stream, verifiable via `/api/audit/verify`; optional field encryption with `SPL_MINOR_STORE_KEY`
- Guardian controls: overview / block / register / export / delete behind a per-session guardian token, plus a verifiable guardian-consent flow (`/api/guardian/challenge` + `/api/guardian/verify`) for under-14 users
- HTTP service layer: Zero dependency `http.server`, default port 8788, **loopback-only bind by default**, session isolation, optional HTTPS

## Usage
### Run Core Engine Directly
```python
import importlib.util
# The engine filename is hyphenated by design, so load it via importlib.
spec = importlib.util.spec_from_file_location("spl_core", "scripts/SPL-anthropic-engine.py")
spl = importlib.util.module_from_spec(spec); spec.loader.exec_module(spl)

core = spl.SPLPureCoreV7_3()   # class name kept for compatibility; this IS the V8.0 behaviour set
# Step 0 — required since v2.6.0: the strict core raises AgeGateBlocked on event entry until confirmed.
core.confirm_age(answer="adult")   # or age=25; a minor/declining answer puts the core in safe mode
# v2.7 optional: opt in to the adaptive personality baseline (default OFF).
core.baseline_adaptation = True    # or pass baseline_adaptation=True to the constructor
# Input event vector: belonging 0.5, threat -0.1, time step 1.0
core.process_vector({"belonging": 0.5, "threat": -0.1}, 1.0)
# Get current full state snapshot
print(core.snapshot())
# Gate state lives outside the snapshot (normative key set is frozen):
print(core.age_gate_state())
```

### Replay / CI harnesses
Any existing harness driving the full-range core must add the `confirm_age()` call before it feeds events, otherwise the first `process_vector()` / `process_event()` / `expect()` raises `AgeGateBlocked`. Inject a virtual clock (`set_clock` / `advance_clock`) as before — bit-exact replay is unchanged by the gate, and the upstream `tests/conformance_vectors.json` baselines still match the shipped cores key-for-key.

### Custom Personality Configuration
```python
import importlib.util
# Reference-only module — NOT wired into the core (upstream: docs/agent-standard.md §4.5)
spec = importlib.util.spec_from_file_location("identity", "assets/feature-guide/Identity module.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

identity = m.IdentityEngine()
identity.add_identity("Poet", strength=0.9)   # strength is a float, not a dict
```

### Language Style Rendering
```python
# Load language style module directly
import importlib.util
spec = importlib.util.spec_from_file_location("lang_style", "assets/feature-guide/language style.py")
lang = importlib.util.module_from_spec(spec); spec.loader.exec_module(lang)
# Generate style instructions based on SPL Core snapshot
# render_style() is a method of LanguageStyleEngine, not a module-level function
style_engine = lang.LanguageStyleEngine()
style = style_engine.render_style(core.snapshot())
print(style.prompt_injection)
```

### Minor Protection Engine
```python
# Run weakened core engine
# python "assets/minor-protection/SPL-anthropic-minor-engine.py"
#
# Or start minor protection HTTP service (port 8788)
# python "assets/minor-protection/SPL-anthropic-minor-server.py"
```

## v2.0 Upgrade Capabilities (P0-P2)

### 💾 Personality State Persistence (P0)
Cross-session continuous personality requires state persistence. Follow `references/PersonaPersistence.md`: State Schema (four blocks: cognition/emotion/motivation/social), atomic writes, schema version migration, determinism guarantee (temperature=0 core decision + seeded randomness).

### 🎭 Emotion-Behavior Mapping (P0)
Projects internal emotional states into observable behaviors (body language/microexpressions/gaze/line style). Refer to the six-state mapping table in `references/EmotionBehaviorMap.md`; isomorphic with the posture mapping in Section D of the AI Drawing Composition Template — personality states can directly drive character image generation.

### ⚖️ Motive Conflict Engine (P2)
Deterministic adjudication during multi-motive competition: Safety constraints → temperament alignment → weighted utility → recency/persistence → user override. Full audit trail for the entire decision process (`references/MotiveConflictRules.md`), auditable, no probability.

### 💬 Conversational Adaptation (P1)
Continuous personality can be directly connected to conversational image/text models (GPT-4o / Gemini): Provide personality state snapshot in the first round, subsequent single-point corrections without changing core anchors.

### 🔌 Soulmate Integration (P1)
The engine can be used as the inference kernel for the your-soulmate extension: The extension handles UI/interaction, the engine handles state evolution, state files are synchronized bidirectionally (see persistence contract).

## v2.2 Upgrade Highlights

- **SPL Core synchronized with latest GitHub version**: Added deterministic audit log (AuditLogger, local JSONL, failures do not block engine)
- **language style.py significantly enhanced**: Added dynamic multi-dimensional tone rendering + deterministic line generation (+234 lines)
- **Added minor protection engine** (`assets/minor-protection/`): Weakened core + HTTP service layer, three-layer protection architecture
- **Deleted obsolete files**: `language-style-demo.py`, `spl-chat-server.py` (replaced by minor-server)
- **Added LICENSE**: Dual-track licensing (free for personal research / commercial authorization required for government/enterprise)
- **README synchronized with latest repository version**

## v2.1 Upgrade Highlights

- **SPL Core synchronized with latest GitHub version**: Completed fields such as `rationalization_load`
- **Added language style module** (`assets/feature-guide/language style.py`): Discrete gear expression personality + style profile + state-to-line rendering
  > Renamed from `assets/feature/` — these modules are **reference guidance only**, not wired into the core (they emit a `tension_base` key outside the vector contract).

## Files
- `references/PersonaPersistence.md` (P0 state persistence contract)
- `references/EmotionBehaviorMap.md` (P0 emotion-behavior mapping table)
- `references/MotiveConflictRules.md` (P2 motive conflict adjudication rules)
- `scripts/SPL-anthropic-engine.py` (Core engine + NarrativeMapper + AuditLogger + age gate + LLM adapters)
- `assets/feature-guide/` (Identity / goals / values / biases / world / language-style modules — **reference only, NOT wired into the core**; see `docs/agent-standard.md` §4.5 upstream)
- `assets/minor-protection/SPL-anthropic-minor-engine.py` (protected core + age gate)
- `assets/minor-protection/SPL-anthropic-minor-server.py` (loopback HTTP service, consent/guardian/crisis flows)
- `assets/minor-protection/COMPLIANCE.md` (mapping to the PRC anthropomorphic-interaction service measures)
- `assets/sujin-demo.md` (worked persona demo — documentation, not runtime code)
- `LICENSE` (Dual-track licensing agreement, v1.2)

At runtime the server additionally creates `data/minor_protection.db` and `logs/*.jsonl` under its own directory unless `SPL_MINOR_DATA_DIR` / `SPL_LOG_DIR` point elsewhere. Neither path is part of the shipped package (`.clawhubignore` excludes them).

## Notes
- Pure Python standard library implementation, no additional dependencies required, Python ≥ 3.8. The single optional package is `cryptography`, used **only** to encrypt stored fields when `SPL_MINOR_STORE_KEY` is set; without it the server falls back to masking (no crash, no outbound call).
- Deterministic **local core**: the same inputs produce the same outputs — no random numbers, no LLM calls, no outbound network. Replay requires an injected virtual clock.
- The **age gate is part of the state machine**, not of the numerics: confirming adulthood changes no state variable, so gated and ungated runs of the same event sequence produce the same snapshots.
- The optional remote LLM adapters are **non-deterministic and OFF by default**; they are outside the guarantee above and never participate in state evolution.
- Licensing: Dual-track model — free for personal non-commercial research, government/enterprise commercial use requires written authorization, see `LICENSE` for details
