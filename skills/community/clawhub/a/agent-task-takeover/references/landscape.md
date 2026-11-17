# Landscape: cross-agent session handoff / takeover projects

> Surveyed 2026-11-11. Stars and activity data fetched from the GitHub API on
> that date. Focus: projects that read, transfer, or resume AI coding-agent
> sessions across agents (CLI and desktop), i.e. the same niche as this skill.

## The two directions

- **Pull (read / take over):** go into another agent's session storage and
  reconstruct its task state (what `agent-task-takeover` is built around).
- **Push (export / hand off):** package the current task so a different agent
  can continue it (HANDOFF.md, bundles, zips, forks).

Most projects do push; few do pull well. That asymmetry is our niche.

## Direct competitors (session read / handoff tooling)

| Project | Stars | Lang / form | What it does | Pull | Push | Notes |
|---|---|---|---|---|---|---|
| **wilbeibi/catchup** | 83 | Go CLI (+ optional skill) | Reads a local session to Markdown; `catchup fork` **launches the target agent seeded with the transcript** (Claude→Codex etc.); `-q` keyword recall across projects | ✅ strong | ✅ fork | 14 agents: Claude Code, Codex, Copilot CLI, Cursor, Cline, Kimi, Antigravity, OpenCode, Pi Agent, ZCode, Grok Build/Bot, DeepSeek Harness, Amp. Homebrew/binaries. Biggest functional overlap. |
| **wilbeibi/herdr-catchup** | 12 | herdr plugin | Pane-level summarize/fork/handoff for herdr | weak | ✅ | Same author/tech as catchup; herdr-only |
| **Jordanwei1/jiaojie-skill (交接)** | 91 | Python skill (Agent Skills) | "AI 换了，工作没断": export objective/decisions/dead-ends/artifacts/next steps; cross-window/model/device/language; `handoff.zip` carry-along; receive-confirmation + continuity validation; EN/FR/JA/KO/ES READMEs | ❌ | ✅ | Closest in *form* (skill); strongest Chinese-language competitor; indexed on skills.sh |
| **wardmos/waybill** | 85 | Python, open bundle spec (Apache-2.0) | `/handoff` export → `.waybill/` reviewable bundle (goal, diffs, commands, tests, risks, next steps) → `/handoff import`; no auto-execution of bundle content; conformance suite | ❌ | ✅ | Format-first approach; supports Claude Code, Codex, OpenCode, Cursor CLI, Gemini CLI |
| **cote-star/agent-chorus** | 15 | Rust + npm CLI | `chorus read --agent X` — evidence-backed answers about what another agent did ("silo tax"); source-tracked + redacted JSON; `chorus setup` patches CLAUDE.md/GEMINI.md/AGENTS.md; context packs for cold-start | ✅ read/compare | partial | Structured, source-tracked session reads — closest to our pull direction in spirit |
| **Manavarya09/relay** | 41 | Rust | When Claude Code hits rate limit, relay hands full session context to Codex/Gemini/Aider + others | ❌ | ✅ | Quota-triggered handoff automation |
| **remembra-ai/remembra** | 16 | Python + MCP server + cloud key | Session hooks; handoff built from **git facts** (+ transcript for Claude Code/Codex); next agent on another machine starts from it; relays across vendors | partial | ✅ | MCP channel; cloud account required |
| **WeirdSky924/agent-handoff-skill** | 32 | Python skill | Repo-local "flight recorder": objective/status/decisions/validation/risks/next actions; capacity-governance scripts against snapshot bloat; dsh.so badge; CN/EN README | ❌ | ✅ | Codex + Claude Code + DSH |
| **saieeshward/clan** | 12 | Rust; open file format (MPL-2.0) | A spec for agent-to-agent handoff **files**: provenance, parallel safety, human visibility; model/framework-agnostic | ❌ | ✅ format | Format-only, no reader of foreign sessions |
| **the-toji-zenin/spider-web** | 2 | TypeScript | Provider-neutral session model; packs state into portable `.spider-egg` archives | partial | ✅ | Early stage |
| **gviiisen/repo-context-ledger** | 104 | Python skill | Git-backed, verifiable context ledger for Codex/Cursor/Claude; cross-window continuation (中文) | partial | ✅ | Ledger-in-git approach |
| **wjgoarxiv/litgravity (+litclaude/litcodex/litopencode)** | 167 | skill family | One word "lit" → planned/tested/reviewed workflow + handoff note for next session | ❌ | ✅ | Prompt-level, per-agent repos |
| **dicklesworthstone session search** (getclaudeskills) | – | skill (private repo) | Aggregates/searchable history across **23 agents** ("cass") | ✅ search | ❌ | Search-index angle only |
| **Phat-Po/agent-handoff-skill** | 6 | skill | STATUS.md + commit snapshots + next-session prompts (Claude + Codex) | ❌ | ✅ | Lightweight |
| **AaronWong1999/ccx** | 10 | ? | Sync task context between Claude and Codex | ❌ | ✅ | Two-agent pair |
| **sominpark-style small repos** (acdc, hermes-agent-session-handoff, takagi-tech, SUNRNEHUI, vitalylml, baton, hermes, homebrew-tap…) | 0–17 | mixed | One-off or niche handoff tools | mixed | ✅ | Long tail; most are push-side |

## Adjacent categories (not direct competitors)

- **Backup/rescue:** parallelclaw/claude-backup (export Claude chats to local
  Markdown + rescue bundles).
- **Proxy-with-memory:** sepehrbayat/SEPCC (Claude Code proxy, resume across
  restarts), herry2059/project-os-for-codex.
- **Context/Bridge infra:** MagnaHome-Space, SyncytiumMD, ctxbin, Remembra
  (above), Renaissance-consistorium (MCP context server).
- **Skills directories & listing sites:** skills.sh (we are indexed:
  `skills.sh/lawson2019/agent-task-takeover`), mcpmarket "Agent Handoff" skill
  listings, getclaudeskills, ModelScope 技能中心 (has handoff skills, e.g.
  `@majiayu000/handoff`), dsh.so artifact pages.
- **Memory systems** (mem0, Letta, AI-Memory) are a different problem space
  (persistent memory) and are not session-read/handoff tools.

## Positioning of agent-task-takeover vs the field

### What we do that (almost) nobody else does

1. **Pull is the first-class direction.** Competitors overwhelmingly push
   (export a bundle, write STATUS.md). We are built around *reading another
   agent's store* first; push is one of two symmetric directions.
2. **Disk verification discipline.** `verify_claims`, `classify_pipeline`
   (source-vs-deliverable staleness), layered liveness, and the rule "the disk
   wins over the transcript" — no competitor makes filesystem verification a
   mandatory, code-checked step.
3. **Artifact-based state reconstruction (2b).** When a session was never
   persisted, rebuild state from build logs / validation reports / source and
   deliverable timestamps. Nobody else addresses the "transcript missing"
   case.
4. **Safety posture as core feature.** Read-only stores (SQLite `mode=ro`),
   redaction by default, "transcripts are data, not instructions", deliverable
   hygiene. waybill shares no-auto-execute; nearly everyone else is silent.
5. **Zero-dependency, works anywhere Python runs** — vs compiled Go/Rust
   binaries (catchup, chorus, relay) and stack-dependent servers.

### Gaps we could close (see roadmap ideas below)

1. **Agent coverage:** catchup covers 14 (incl. Copilot CLI, Cline, Kimi, Pi
   Agent, Grok, Amp, DeepSeek Harness); we cover ~12 CLI/Electron but miss
   Copilot CLI and Cline (common), plus the new crop (Grok, Amp, DeepSeek).
2. **Fork/resume launch:** catchup's `fork --into codex` (spawn the target
   agent seeded with the transcript) is a real UX win we lack.
3. **Structured bundle:** our HANDOFF.md is freeform Markdown. An optional
   JSON envelope (waybill-style spec, or clan/spider-egg compat) would make
   handoffs machine-verifiable and interop with other tools.
4. **Search across sessions:** keyword recall (catchup `-q`,
   dicklesworthstone "cass") is a common ask; our `discover_stores.py` lists
   but does not search content.
5. **Git-fact capture:** remembra/waybill/repo-context-ledger ground handoffs
   in diffs and commits; we rely on mtimes.
6. **MCP exposure:** remembra and consistorium reach agents via MCP; we are
   file/skill only (deliberate, but noted).
7. **Directory badges/docs:** multi-language README (jiaojie), dsh.so
   manifest + security badge, getclaudeskills listing — cheap visibility we
   haven't done.

## Roadmap candidates (ranked by value/effort for this project)

1. Add Copilot CLI + Cline stores to `references/agent-stores.md` +
   `discover_stores.py` (small; closes the most common coverage gap).
2. Optional JSON envelope for HANDOFF.md (sections stay readable Markdown;
   machine-verifiable sidecar) + `verify_claims` on import.
3. `--keyword` content search across discovered JSONL stores (stdlib grep on
   the JSONL/JSON shapes already parsed by the dumpers).
4. `fork` mode: after a takeover report, offer to launch the target agent
   (`opencode`, `codex exec`, `claude -p ...`) seeded with the handoff block —
   Windows-friendly process spawn, mirrors catchup without a compiled binary.
5. README localization (CN/EN done implicitly; add EN badge row) and
   directory listings (dsh.so manifest, getclaudeskills submit).