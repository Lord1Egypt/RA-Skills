---
name: benchmark-model-provider
description: Benchmark and rank AI providers/models against a user-specific prompt suite derived from the user's purpose, domain, and usage frequency. Use when users ask which model is smarter, cheaper, deeper, faster, worth using daily, better as local vs service, or when building repeatable benchmark specs, reranking old runs, generating markdown/HTML/PDF benchmark reports.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"],"env":["BENCHMARK_API_KEY"]},"primaryEnv":"BENCHMARK_API_KEY"}}
---

# Benchmark Model Provider

> Use this skill to help users choose the most suitable model for their own workflow instead of giving generic “best model” advice.

**Tiếng Việt**  
Dùng skill này khi Boss muốn biết model nào thật sự đáng dùng cho workflow hằng ngày: model nào research tốt hơn, viết báo cáo ổn hơn, code ngon hơn, rẻ hơn, nhanh hơn, hay đáng dùng lâu dài hơn. Skill này không trả lời kiểu cảm tính, mà dựng benchmark theo đúng nhu cầu thực tế của người dùng rồi chấm, rerank và xuất report rõ ràng.

**中文说明**  
当用户想知道“哪个模型更聪明、更便宜、更适合日常工作流、更适合研究/写报告/编程”时，使用这个技能。它不会给出泛泛而谈的“最佳模型”建议，而是根据用户自己的实际任务构建基准测试，保留原始结果、重新排序，并生成可审阅、可分享的报告。

Treat the benchmark as a **personal decision framework**:
- derive the benchmark from the user's real work
- keep the run auditable
- preserve raw outputs for reranking
- generate outputs that can be reviewed, shared, and published cleanly

---

## What this skill is for

People often ask questions like:
- Which model is smarter?
- Which model is cheaper to run daily?
- Which model is deeper or more useful for my job?
- Should I use a local model or a service model?

This skill exists to answer those questions with a **repeatable benchmark process**, not with vague preferences.

---

## Core operating flow

1. **Collect benchmark context**
   - purpose
   - domain
   - usage frequency
2. **Build or select a benchmark spec** with 5–10 domain-specific questions
3. **List currently available providers/models** from trusted local OpenClaw context when allowed
4. **Ask whether the user wants to use the current list or add more models**
5. **Verify every user-supplied model before running**; if the name does not match, ask again or suggest the closest valid model id
6. **Run each model independently** on the same benchmark set
7. **Preserve raw outputs and metrics** so the run can be audited and reranked later
8. **Score results** across quality, depth, cost, and speed metrics
9. **Build reports** in markdown / HTML / PDF
10. **Optionally** suggest simple ways to publish the generated HTML report (Vercel, Netlify, Cloudflare Pages, GitHub Pages) if the user wants a shareable link

---

## Default decisions

| Area | Default |
| --- | --- |
| Benchmark mode | `prompt_only` |
| Overall scoring | quality + depth + cost |
| Speed handling | measured and reported, excluded from default overall |
| Execution strategy | `sequential` unless orchestration is needed |
| Web publish target | (no built-in publish) — suggest Vercel / Netlify / Cloudflare Pages / GitHub Pages |

---

## Workflow rules

### Benchmark input rules
- Default to `prompt_only` unless the user explicitly wants `agent_context`.
- In `prompt_only`, send only the raw prompt.
- Do **not** inject extra context, memory, few-shot examples, or hidden scaffolding in `prompt_only` mode.
- In `agent_context`, use one fixed shared system/context layer for all compared models and record it in metadata.

### Execution rules
- Support both `sequential` and `subagent_orchestrated` execution strategies.
- Allow bounded parallel execution for subagents (for example `--max-parallel 4`) when the endpoint can tolerate it.
- Treat `rerank` as a first-class operation; do not rerun models when only the scoring formula changes.
- Report progress at every major step so the user never feels the process is hanging.
- During batch execution, surface a clear update whenever one agent/model finishes.
- Normalize model ids before calling the endpoint when the provider catalog exposes raw model ids but the user/runtime spec may contain provider-prefixed names.
- If the endpoint returns naming/provider mismatch errors, explain the mismatch clearly instead of leaving only a raw 502/unknown-provider error.

### Output rules
- Mark every estimated metric clearly.
- Rewrite reports/landing pages to the newest snapshot.
- Do **not** append patch fragments to stale output.
- Reports should include: ranking table, cost table, executive summary, overall assessment, recommended model selection, and full answer details.
- Default the report language to the user's current conversation language.
- Only switch the report language when the user explicitly asks for a different language or a bilingual output.
- PDF output must use Unicode-capable fonts so Vietnamese, Chinese, and multilingual content render correctly.
- Multilingual support means the renderer can display multiple languages correctly; it does **not** mean the skill should arbitrarily change the report language.
- Ask before delivering externally via Vercel or other web publishing.

---

## Safety and trust boundary

> This skill may perform network I/O depending on how the benchmark spec is configured.

### Safe-by-design intent
- Example specs should use placeholder endpoints, not a private hardcoded runtime.
- The user should supply only trusted API endpoints and credentials.
- Publishing should happen only when the user explicitly wants delivery.

### Important runtime notes
- `run_benchmark.py` sends prompts to the `base_url` configured in the benchmark spec.
- This skill does **not** publish to Vercel/Netlify/Cloudflare/GitHub automatically. It only generates local HTML/PDF artifacts.
- If you want a shareable link, publish the generated HTML folder using one of these services: Vercel, Netlify, Cloudflare Pages, or GitHub Pages.
- Only run the skill with endpoints, tokens, and outputs you trust.

For detailed runtime assumptions, read:
- `references/runtime-safety.md`
- `references/environment-vars.md`
- `references/pricing-sources.md`

---

## What to read

Read only what you need:

- `references/initial-project-spec.md` — authoritative design baseline
- `references/benchmark-schema.md` — benchmark spec structure, run artifacts, file layout
- `references/scoring-rubric.md` — scoring model, normalization rules, default weights
- `references/pricing-sources.md` — pricing precedence and estimation policy
- `references/execution-modes.md` — benchmark modes, execution strategies, operational modes
- `references/output-modes.md` — delivery choices, publish rules, progress feedback rules
- `references/runtime-safety.md` — trust boundaries, network behavior, safe usage guidance
- `references/environment-vars.md` — expected environment variables and dependency notes
- `examples/*.yaml` — benchmark context templates and ready-made examples in multiple languages

---

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/build_benchmark_spec.py` | Build a benchmark spec from benchmark context |
| `scripts/run_benchmark.py` | Execute benchmark runs and write raw outputs/metrics |
| `scripts/estimate_tokens.py` | Estimate token counts when provider usage is missing |
| `scripts/resolve_pricing.py` | Resolve pricing sources and compute estimated/official pricing |
| `scripts/score_models.py` | Combine raw metrics and rubric scores into rankings |
| `scripts/build_report.py` | Build markdown, HTML, and PDF report artifacts |
| `scripts/publish_report.py` | No deployment automation. Export/copy PDF and print suggested static hosting options (Vercel/Netlify/Cloudflare Pages/GitHub Pages). |

---

## Output contract

Try to produce these artifacts whenever possible:

- versioned benchmark spec
- raw per-model answer files
- raw metrics JSON
- score breakdown JSON
- markdown summary report
- HTML landing page
- PDF output when requested
- publish result metadata when delivery occurs
