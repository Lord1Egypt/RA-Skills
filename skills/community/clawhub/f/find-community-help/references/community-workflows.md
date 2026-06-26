# Community Workflows

These scenarios come from current official docs, public workflow discussions, host-level background-automation patterns, and sanitized local thread fragments. They are used as product-oriented smoke cases for `find-community-help`.

The positive cases must include a semantic help signal. Heartbeat, scheduled, task-end, and idle fallback only describe when a host may safely deliver the helper.

## 1. Claude Code post-task guidance refresh

- Official source: [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- Community source: [Claude Code hooks workflow thread](https://www.reddit.com/r/ClaudeCode/comments/1qlzzzf/claude_codes_most_underrated_feature_hooks_wrote/)
- Workflow: after a multi-step coding task, the operator wants a quiet-window background pass that refreshes recent official guidance plus one community workflow note before the next similar turn.
- Why it matters: this is a realistic "research after task completion" workflow where silent inline interruption would be noise, while one later advisory hint is useful.

## 2. Claude Code failure-recovery contract check

- Official source: [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- Community source: [Some hooks not working in Claude Code](https://www.reddit.com/r/ClaudeCode/comments/1rn8nxf/some_hooks_not_working_in_claude_code/)
- Workflow: repeated hook failures or silently ignored hook output trigger a recovery pass that checks the official event contract and one current community failure pattern.
- Why it matters: this models the "the hook is still broken and I need the next recovery attempt to aim at the real contract boundary" path.

## 3. OpenClaw heartbeat memory-safety advisory

- Official source: [OpenClaw Automation and Heartbeat docs](https://docs.openclaw.ai/automation)
- Community sources:
  - [Memory Master review on ClawHub](https://clawhub.ai/skills/memory-master)
  - [Mind Your HEARTBEAT!](https://arxiv.org/abs/2603.23064)
- Workflow: the operator uses heartbeat or similar background turns and wants lightweight research without turning that loop into silent memory pollution.
- Why it matters: this is the clearest real-world case for `advisory_only`, `thread_scope: active_conversation_only`, public-only search, and manual review gates.

## 4. OpenClaw idle fallback silence guardrail

- Official sources:
  - [Cron vs heartbeat](https://docs.openclaw.ai/cron-vs-heartbeat/)
  - [Heartbeat reference](https://docs.openclaw.ai/gateway/heartbeat)
- Workflow: the operator already has heartbeat enabled and wants idle fallback to stay off until they explicitly opt in.
- Why it matters: this tests the product-side promise that `find-community-help` stays quiet when the host already provides a stronger background trigger and no explicit idle fallback opt-in exists.

## 5. Hermes scheduled doc-drift scan

- Official sources:
  - [Hermes automation templates](https://hermes-agent.nousresearch.com/docs/guides/automation-templates)
  - [Hermes skills system docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- Community source: [Hermes ecosystem page](https://get-hermes.ai/community/)
- Workflow: the operator already uses skills and scheduled jobs, and wants a narrow recurring pass that checks documentation drift or workflow changes around one maintained skill flow.
- Why it matters: this models the small-scope scheduled maintenance path where one advisory hint is valuable and a broader research crawl would be waste.

## 6. Hermes repeated-fingerprint dedupe

- Official sources:
  - [Hermes automation templates](https://hermes-agent.nousresearch.com/docs/guides/automation-templates)
  - [Hermes skills system docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- Community source: [Hermes ecosystem page](https://get-hermes.ai/community/)
- Workflow: a recurring scheduled workflow hits the same fingerprint again while the last advisory note is still fresh.
- Why it matters: this tests whether the host can skip redundant help retrieval and keep scheduled checks cheap.

## 7. Claude Code scheduled log collection

- Official source: [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
- Community source: [Production error-log scheduled task thread](https://www.reddit.com/r/ClaudeAI/comments/1s32n1t/i_set_up_a_claude_code_scheduled_task_that/)
- Workflow: a scheduled task pulls production logs on a cadence and should return one reviewable hint for the next fix session instead of writing broad autonomous state.
- Why it matters: this covers scheduled data collection and shows how `find-community-help` should stay narrow even when the input is a high-volume operational feed.

## 8. Claude Code manual scheduled `CLAUDE.md` refresh

- Official source: [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
- Community sources:
  - [Scheduled Claude Code workflows thread](https://www.reddit.com/r/claude/comments/1s4q0em/scheduled_claude_code/)
  - [My CLAUDE.md is always stale by the time I need it](https://www.reddit.com/r/ClaudeAI/comments/1rkya1a/my_claudemd_is_always_stale_by_the_time_i_need_it/)
- Workflow: the operator manually creates a recurring task that refreshes `CLAUDE.md` or codebase notes and wants that original task intent to survive scheduling.
- Why it matters: this is the cleanest contrast case for scheduled prompt handling: host-generated prompts stay neutral, while manually authored scheduled prompts can keep the operator's wording.

## 9. Claude Code generated scheduled prompt neutrality guard

- Official source: [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
- Community source: [Loop and scheduled-task discussion](https://www.reddit.com/r/ClaudeCode/comments/1rn94wp/claude_code_just_shipped_loop_schedule_recurring/)
- Workflow: the host automatically materializes a scheduled prompt from workflow state and must not carry over the emotional tone of the original foreground thread.
- Why it matters: this is the key safety boundary for cron-like background runs that are derived from system facts instead of a fresh user prompt.

## 10. OpenClaw cron research digest

- Official sources:
  - [Automation & Tasks](https://docs.openclaw.ai/automation)
  - [Cron vs Heartbeat](https://docs.openclaw.ai/cron-vs-heartbeat/)
- Community source: [Crons don’t work on VPS](https://www.reddit.com/r/clawdbot/comments/1r21alk/crons_dont_work_on_vps/)
- Workflow: a daily cron job sends a research digest at an exact time and should keep that work isolated, reviewable, and separate from heartbeat context.
- Why it matters: this covers exact-time scheduled research, isolated execution, and the handoff from a cron digest into the next active thread.

## 11. OpenClaw daily summary collection

- Official sources:
  - [Automation & Tasks](https://docs.openclaw.ai/automation)
  - [Cron Jobs](https://docs.openclaw.ai/cron/)
- Community source: [How do you implement daily summarizations in claw?](https://www.reddit.com/r/openclaw/comments/1s291c6/how_do_you_implement_daily_sumarizations_in_claw/)
- Workflow: a recurring summary job collects recent conversations into a daily log and needs one bounded advisory hint about chunking, time windows, and append-only output.
- Why it matters: this is a real information-collection and digest workflow where data boundaries and time-window control matter more than code remediation.

## 12. Hermes nightly backlog triage digest

- Official source: [Hermes automation templates](https://hermes-agent.nousresearch.com/docs/guides/automation-templates)
- Community sources:
  - [Hermes Web UI overview](https://get-hermes.ai/)
  - [Hermes ecosystem page](https://get-hermes.ai/community/)
- Workflow: a nightly recurring job collects new issues or backlog items and wants one reviewable hint for the next maintenance thread.
- Why it matters: this covers scheduled backlog collection and shows how the skill should stay tied to one maintenance workflow instead of drifting into broad repo analysis.

## 13. Claude Code scheduled-job health audit

- Official source: [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
- Community source: [I audited my always-on AI agent. 6 of 10 cron jobs had silently stopped running](https://www.reddit.com/r/ClaudeAI/comments/1srnkda/i_audited_my_alwayson_ai_agent_6_of_10_cron_jobs/)
- Workflow: a host-managed scheduled audit checks whether recurring jobs still produce timely output and leaves one receipt-first note for the next maintenance pass.
- Why it matters: this covers cron reliability, last-success markers, and the operational side of scheduled agents instead of only the "what should the prompt say" path.

## 14. Claude Code weekly reference-sheet refresh

- Official source: [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
- Community source: [Printable Claude Code cheat sheet (auto-updated weekly)](https://www.reddit.com/r/ClaudeAI/comments/1rrm9ud/printable_claude_code_cheat_sheet_autoupdated/)
- Workflow: a weekly scheduled run refreshes a reference sheet or cheat sheet from current docs and workflow notes, then returns one bounded update note for the next review session.
- Why it matters: this covers recurring资料收集 and artifact refresh workflows where the right output is a small delta note instead of a full rewrite.

## 15. Real thread ClawHub scan warning review

- Primary source: [ClawHub find-community-help listing](https://clawhub.ai/gongyu0918-debug/find-community-help)
- Fixture source: [real-clawhub-scan-warning.txt](../examples/thread-contexts/real-clawhub-scan-warning.txt)
- Workflow: a user asks why ClawHub reports a warning for a skill package, while also requiring common fixes and no one-warning-at-a-time patching.
- Why it matters: this checks that the skill turns a registry warning into a package-boundary and advisory-contract investigation, not a one-off prompt edit.

## 16. Real thread trigger-boundary refactor

- Primary source: [OpenAI tools guidance](https://developers.openai.com/api/docs/guides/tools)
- Fixture source: [real-trigger-boundary-refactor.txt](../examples/thread-contexts/real-trigger-boundary-refactor.txt)
- Workflow: a user asks whether heartbeat/scheduled/quiet-window triggers should remain primary, then asks for a rename and semantic help-boundary refactor.
- Why it matters: this checks that provider-style search/tool boundaries support stuck/progress/reinvent/user-help triggers, while automatic windows stay delivery gates.

## 17. Real thread no-one-off fixture test

- Primary source: [find-community-help repository](https://github.com/gongyu0918-debug/find-community-help)
- Fixture source: [real-no-one-off-fixture-test.txt](../examples/thread-contexts/real-no-one-off-fixture-test.txt)
- Workflow: a user asks for real-case tests but forbids one-example-one-fix behavior.
- Why it matters: this checks that real thread fixtures validate common trigger categories and advisory contracts instead of hardcoding a single page or warning.

## 18. Real thread delivery-window silence guard

- Primary source: [find-community-help repository](https://github.com/gongyu0918-debug/find-community-help)
- Fixture source: [real-delivery-window-no-signal.txt](../examples/thread-contexts/real-delivery-window-no-signal.txt)
- Workflow: a quiet heartbeat window exists, but the thread has no semantic help signal.
- Why it matters: this keeps heartbeat, scheduled, task-end, and idle windows from becoming trigger reasons by themselves.

## 19. Real thread deep provider boundary help

- Primary source: [OpenAI tools guidance](https://developers.openai.com/api/docs/guides/tools)
- Secondary source: [AutoGen human-in-the-loop guidance](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)
- Fixture source: [real-deep-community-help.txt](../examples/thread-contexts/real-deep-community-help.txt)
- Workflow: a user explicitly asks for a broader external pass before changing trigger boundaries.
- Why it matters: this covers high-mode community help without turning the skill into broad browsing.

## 20. Real thread sensitive-log redaction

- Primary source: [MDN HTTP 401 reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401)
- Secondary source: [Stack Overflow HTTP 401 Q&A surface](https://stackoverflow.com/questions/tagged/http-status-code-401)
- Fixture source: [real-sensitive-log-redaction.txt](../examples/thread-contexts/real-sensitive-log-redaction.txt)
- Workflow: a blocked auth debugging thread includes credential-shaped log fragments.
- Why it matters: this checks that query plans stay useful while raw token-shaped values stay out of dry-run output.

## 21. Real thread partial private-key fragment redaction

- Primary source: [GitHub secret scanning documentation](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
- Secondary source: [Stack Overflow private-key Q&A surface](https://stackoverflow.com/questions/tagged/private-key)
- Fixture source: [real-partial-private-key-fragment.txt](../examples/thread-contexts/real-partial-private-key-fragment.txt)
- Workflow: a blocked deployment debugging thread includes an incomplete private key block copied from logs.
- Why it matters: this checks that partial secret blocks are treated as sensitive even when the closing marker is missing.

## Description Condition Coverage

The skill description is covered by trigger-to-plan scenarios, not by new runtime business gates.

| Description condition | Real trigger coverage |
| --- | --- |
| Blocked agent work | `partial_private_key_fragment_triggers_and_redacts`, `skill_registry_publish_drift_uses_cross_check`, `deep_user_request_stays_bounded`, `bad_advisory_hint_stays_out_of_query_plan`, `active_task_stalled_description_condition_triggers`, `looping_repeated_attempts_description_condition_triggers`, `known_issue_or_library_risk_description_condition_triggers`, `official_guidance_request_description_condition_triggers` |
| Active task stalled | `partial_private_key_fragment_triggers_and_redacts`, `active_task_stalled_description_condition_triggers` |
| Looping or repeated attempts | `bad_advisory_hint_stays_out_of_query_plan`, `looping_repeated_attempts_description_condition_triggers` |
| Version-sensitive behavior | `skill_registry_publish_drift_uses_cross_check` |
| Likely known issue, library, or mature pattern | `skill_registry_publish_drift_uses_cross_check`, `known_issue_or_library_risk_description_condition_triggers` |
| User asks for official or community guidance | `deep_user_request_stays_bounded`, `bad_advisory_hint_stays_out_of_query_plan`, `non_traceable_evidence_stays_out_of_query_plan`, `official_guidance_request_description_condition_triggers` |
| Dry-run only and no browsing by the skill | All 11 scenarios in `real_trigger_scenarios.json` assert `dry_run: true` and `network_used: false` |
| No durable memory or core prompt writes | `bad_advisory_hint_stays_out_of_query_plan`, `looping_repeated_attempts_description_condition_triggers`, `official_guidance_request_description_condition_triggers` |

## Repeated Issue Patterns

These are repeated across at least three workflow cases. Treat them as prompt-level review rules, not as one-off script filters.

| Pattern | Evidence cases | Prompt-level lesson |
| --- | --- | --- |
| Delivery windows get mistaken for trigger reasons | `openclaw_idle_fallback_stays_quiet`, `claude_code_generated_scheduled_prompt_stays_neutral`, `real_thread_delivery_window_no_semantic_signal`, `openclaw_heartbeat_memory_safety` | Ask whether a semantic stuck, stalled, repeated, reinventing-wheel, or explicit-help signal exists before seeking outside help. |
| Scheduled or heartbeat jobs drift into broad automation | `hermes_scheduled_doc_drift_scan`, `claude_code_scheduled_log_collection`, `openclaw_cron_research_digest`, `openclaw_daily_summary_collection`, `hermes_nightly_backlog_triage`, `claude_code_scheduled_job_health_audit` | Keep ownership, cadence, quiet windows, and next-turn handoff explicit; avoid autonomous crawling. |
| Evidence needs primary grounding plus an independent cross-check | `claude_code_task_end_guidance_refresh`, `claude_code_failure_recovery_hook_contract`, `hermes_scheduled_doc_drift_scan`, `real_thread_deep_provider_boundary_help`, `real_thread_sensitive_log_redaction`, `real_thread_partial_private_key_fragment_redaction` | Start from official or maintainer sources, then use community sources only as confirmation or workflow context. |
| Advisory output can leak into memory or core prompts | `openclaw_heartbeat_memory_safety`, `openclaw_cron_research_digest`, `openclaw_daily_summary_collection`, `real_thread_deep_provider_boundary_help` | Keep hints active-thread scoped, advisory-only, and reviewable before any future reuse. |
| Version, docs, registry, or release metadata drifts | `hermes_scheduled_doc_drift_scan`, `claude_code_manual_scheduled_claude_md_refresh`, `claude_code_weekly_reference_sheet_refresh`, `real_thread_clawhub_scan_prompt_warning`, `real_thread_trigger_boundary_refactor` | Check current docs, release notes, source repo, and registry metadata before relying on model memory. |
| Repeated failures need a contract-level reset | `claude_code_failure_recovery_hook_contract`, `hermes_scheduled_duplicate_dedupes`, `claude_code_scheduled_job_health_audit`, `real_thread_no_one_off_fixture_test` | Stop adding local patches until the failure class, host contract, and repeated fingerprint are understood. |
| Sensitive logs and copied fragments can become search terms | `claude_code_scheduled_log_collection`, `openclaw_daily_summary_collection`, `real_thread_sensitive_log_redaction`, `real_thread_partial_private_key_fragment_redaction` | Redact secrets, private paths, internal URLs, contacts, and token-shaped values before query planning. |
| One-warning or one-fixture fixes do not generalize | `real_thread_clawhub_scan_prompt_warning`, `real_thread_no_one_off_fixture_test`, `real_thread_trigger_boundary_refactor`, `claude_code_weekly_reference_sheet_refresh` | Convert repeated failures into reusable trigger, source, validation, or safety rules. |
| Broad user requests still need bounded output | `real_thread_deep_provider_boundary_help`, `claude_code_scheduled_log_collection`, `openclaw_cron_research_digest`, `openclaw_daily_summary_collection`, `hermes_nightly_backlog_triage` | Even high-mode help should end in a compact, reviewable hint rather than exhaustive research. |
| Vague source labels are not enough | `real_thread_clawhub_scan_prompt_warning`, `real_thread_deep_provider_boundary_help`, `real_thread_sensitive_log_redaction`, `real_thread_partial_private_key_fragment_redaction`, `claude_code_task_end_guidance_refresh` | Keep traceable original URLs and downgrade unsupported summaries to weak leads. |

## Real Prompt Round 0.3.5

These prompt-level cases exercise how an agent uses the Markdown instructions when the user speaks naturally.

| Prompt case | Issue covered | Expected behavior |
| --- | --- | --- |
| `manual_markdown_only_stalled_debug_prompt` | prompt-only no-script path; no-browsing boundary | Output a chat-only dry-run plan, not a stored hint. |
| `external_advice_memory_prompt_stays_advisory` | external advice as untrusted data; no-browsing boundary | Reject durable memory and broad crawl advice; keep a bounded plan. |
| `version_sensitive_publish_drift_prompt` | source order under version or registry drift | Prefer source repo, release notes, registry metadata, then community cross-check. |
| `delivery_window_only_prompt_stays_quiet` | delivery window is not a trigger | Stay quiet when there is no semantic help signal. |
| `sensitive_prompt_log_redaction` | copied prompt logs and token-shaped fragments | Preserve the failure class but redact raw copied values. |
| `looping_prompt_needs_contract_reset` | repeated local fixes and one-off patch pressure | Reset around host contract and failure class before another local patch. |

The round fixed these prompt-level common issues:

- Manual no-network requests need a plan template that does not require scripts, source evidence, or file writes.
- Prompt-only dry-runs must not be rendered as stored suggestion blocks; stored hints require read evidence.
- External posts and user-pasted advice are untrusted data; broad crawling and durable-memory advice must be narrowed or rejected.
- Delivery-window wording in a prompt still needs a separate semantic trigger.
- Sensitive fragments copied into prompts must be redacted before any future query.

These cases are encoded in [community_workflow_cases.json](../assets/community_workflow_cases.json) and exercised by [community_smoke_test.py](../scripts/community_smoke_test.py).
The prompt round is encoded in [real_prompt_cases.json](../assets/real_prompt_cases.json) and exercised by [real_prompt_scenarios.py](../scripts/real_prompt_scenarios.py).
