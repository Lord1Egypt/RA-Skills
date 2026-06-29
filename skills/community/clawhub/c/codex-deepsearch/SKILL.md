---
name: codex-deepsearch
description: "Use when Codex must run or review deep, source-backed research as a Codex-native workflow: local/web evidence separation, tool-limit disclosure, source and claim ledgers, review gates, spec/roadmap/implementation readiness, /goal checkpointing, privacy-safe repo handling, and optional codex-with-cc-plus or Claude Code worker delegation. Use for evidence-heavy research, current product/API/tool/law/market questions, architecture discovery before implementation, and research that may become a plan, spec, roadmap, PRD, or engineering input."
---

# Codex DeepSearch

Use this skill to make DeepSearch fit Codex's actual runtime: threads, workspaces, tools, skills, file edits, git state, progress updates, `/goal`, validation, and optional delegated workers. The goal is not a long report. The goal is decision-quality evidence that can survive review.

## Minimum Contract

Every Codex DeepSearch run must:

1. Frame the decision question, audience, scope, exclusions, privacy boundaries, source priority, and stop conditions before broad searching.
2. Build a scenario matrix for cases where the answer can differ by role, permission, platform, version, region, plan, local/cloud execution, or implementation path.
3. Keep a source ledger and claim ledger before synthesis; read `references/source-and-claim-ledgers.md` when creating or reviewing them.
4. Label claims as `retrieved_fact`, `source_summary`, `inference`, `needs_verification`, or `conflict`.
5. Never treat search snippets, abstracts, tool summaries, model reasoning, or generated prose as `retrieved_fact`.
6. Separate web/open/browser evidence from local file evidence and user-provided evidence in both ledger and report.
7. Run the review gate in `references/review-gate.md` before final output or before accepting a worker report.
8. State whether the result can become spec, roadmap, product decision, or implementation input; if not, name the blocking gaps.

## Codex Runtime Rules

Read `references/codex-runtime-model.md` when a task involves local files, `/goal`, resuming, long-running research, workspace boundaries, or a dirty worktree.

- Treat `AGENTS.md` and repo docs as maps and constraints, not as proof of external facts.
- Prefer `rg`, `sed`, `git status`, and `git diff` for local inspection.
- Use `apply_patch` for manual edits when the user explicitly asks to create research artifacts or update skill files.
- Do not default to writing inside a project repository. Ask or use an explicitly authorized research directory.
- Do not commit, stage, or push unless the user explicitly asks.
- If Python is needed, use `uv` or an existing project/skill validation command; do not modify system Python.
- In `/goal` mode, keep durable checkpoints: current phase, accepted evidence, unresolved gaps, next checks, and review status.

## Research Workflow

Read `references/research-workflow.md` for the full flow:

```text
frame -> scenario matrix -> source discovery -> source ledger -> claim ledger
-> counter-evidence -> synthesis -> review gate -> handoff/readiness decision
```

Use templates when a durable artifact is useful:

- `templates/RESEARCH_DESIGN.md`
- `templates/SOURCE_LEDGER.md`
- `templates/CLAIM_LEDGER.md`
- `templates/DEEPSEARCH_REPORT.md`
- `templates/REVIEW_GATE.md`

## Tooling And Source Rules

Read `references/codex-tooling-rules.md` before using web/search/browser/MCP, local files, or delegated workers.

- Web search discovers candidates. Opened pages, fetched docs, rendered PDFs, or verified local files support `retrieved_fact`.
- Snippet-only sources stay `source_summary` or `needs_verification`.
- Local file reads must record path, access date, retrieval method, and whether the file is public/project/private/user-provided.
- Record unavailable tools explicitly: web disabled, browser unavailable, WebFetch unavailable, MiniMax MCP unavailable, login/paywall/region blocked, or local file denied.
- When facts may be current or unstable, browse or use official/current sources and record freshness limits.

## Privacy And Repo Safety

Read `references/privacy-and-repo-safety.md` before inspecting user files or writing artifacts.

- Do not read private or ignored material unless the user explicitly authorizes it for this task.
- Treat `workspace/`, `recordings/`, `transcripts/`, `tts/`, `audio/`, secrets, private resumes, salary records, interview logs, `.env`, databases, and obvious personal exports as off limits by default.
- Check `.gitignore` and dirty worktree before writing inside any repo.
- Never use `git add .`.
- Do not upload private local material to remote tools or paste it into web services.

## Optional Delegation

Read `references/delegation-with-codex-with-cc.md` when the user explicitly asks for subagents, worker execution, delegation, `codex-with-cc`, Claude Code, or when a broad research task needs parallel source scouting or independent review and the user permits it.

- `codex-with-cc-plus` and Claude Code are optional worker layers, not required dependencies.
- Main Codex owns the research design, task files, acceptance criteria, final synthesis, and review decision.
- Workers gather evidence or review ledgers; they do not decide final acceptance.
- If the user has `codex-with-cc-plus`, use it to widen search and analysis with bounded researcher/reviewer tasks and exact report requirements.

## Output Status

Use:

- `DONE`: primary/high-quality sources were opened, material claims map to evidence, counter-evidence was checked, and the review gate accepts the result.
- `DONE_WITH_CONCERNS`: useful result, but tool limits, snippet-only claims, stale sources, unresolved assumptions, or manual checks remain.
- `NEEDS_CONTEXT`: the decision question, scenario matrix, private-data authorization, or target audience is too unclear.
- `BLOCKED`: no useful source discovery or permitted local evidence access is possible.

Final reports must make uncertainty visible and must not smooth over missing evidence.
