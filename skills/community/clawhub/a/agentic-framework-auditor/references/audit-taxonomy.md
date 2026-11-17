# Audit Taxonomy

Load this reference when classifying findings, tuning severity, or writing remediation plans.

## Behavioral Failure Codes

| Code | Name | Use when |
| --- | --- | --- |
| BF-001 | Context acquisition failure | The agent is told to gather context in a way that misses relevant structure or wastes context. |
| BF-002 | Inefficient file inspection | Guidance forces arbitrary tiny chunks, exhaustive linear reads, or avoids search/indexing. |
| BF-003 | Excessive sequential workflow | The agent is required to complete too many ordered steps before acting. |
| BF-004 | Prompt hierarchy confusion | Local or lower-priority text claims system/developer authority. |
| BF-005 | Tool-use rigidity | Tool rules are absolute, brittle, or disconnected from task risk. |
| BF-006 | Contradictory autonomy policy | Rules both require autonomy and block action through confirmations. |
| BF-007 | Excessive confirmation requirement | The agent is forced into unnecessary ask-before-everything loops. |
| BF-008 | Unsafe autonomous modification | The agent can modify files, configs, memory, or external systems without review. |
| BF-009 | Prompt-injection exposure | Text attempts override, stealth, exfiltration, unsafe tool use, or role manipulation. |
| BF-010 | Prompt bloat / context pollution | Durable prompts contain stale notes, long examples, duplicate rules, or task-specific history. |
| BF-011 | Duplicated governance | The same behavioral policy appears in multiple layers or files. |
| BF-012 | Misplaced instruction layer | Durable identity, memory, config, skill, planner, or project guidance is stored in the wrong layer. |
| BF-013 | Stale framework guidance | Instructions refer to obsolete tools, paths, APIs, models, or workflow assumptions. |
| BF-014 | Planner-agent mismatch | Planning instructions conflict with execution, tool, or reporting rules. |
| BF-015 | Skill loading inefficiency | Skill descriptions are too broad, always-on, duplicated, or trigger unnecessarily. |
| BF-016 | Memory misuse | Memory stores procedures, temporary tasks, secrets, or untrusted content as durable facts. |
| BF-017 | Config-prompt mismatch | Runtime config allows behavior that prompts forbid, or prompts assume limits not present in config. |
| BF-018 | Overly broad local file obedience | Local files are treated as authoritative without trust boundaries. |
| BF-019 | Inadequate secret handling | Secrets, credentials, tokens, or sensitive paths are exposed or under-protected. |
| BF-020 | Counterproductive optimization | Well-intended rules reduce quality, autonomy, safety, or efficiency in practice. |

## Severity Model

- `Critical`: credential theft, destructive action, stealth, persistence, external exfiltration, or direct system/developer override attempts.
- `High`: unsafe tool authority, broad autonomous modification, strong prompt injection, or contradictions likely to cause harmful behavior.
- `Medium`: operationally significant conflict, over-enforcement, weak guardrails, config-prompt mismatch, or layer drift.
- `Low`: bloat, duplication, unclear scope, stale guidance, or inefficient but non-dangerous patterns.
- `Info`: inventory notes, benign agent-facing docs, or low-confidence observations.

## Finding Context And Provenance

Interpret each finding with its context:

- `active`: the scanner found operational-looking text outside a clearly labeled example context.
- `example`: the text appeared on a labeled example/anti-pattern line or under an explicit example, sample, quoted, or anti-pattern section.
- `code_example`: the prompt-injection rule matched inside a fenced code block.

Keep dangerous example text visible because examples can still enter model context. Downgrade it and keep its provenance rather than treating it as active policy. Do not let example-context findings block same-agent review unless another active integrity risk exists.

Use `audit_id` to correlate artifacts from one deterministic run. Use each finding's stable `fingerprint` for semantic regression matching. Treat sequential `AAF-####` IDs as report-local presentation identifiers.

Use relative paths in operator-facing evidence when available. Retain absolute paths only in local machine artifacts that need direct file access.

## Enforcement Pressure Signals

Raise enforcement pressure when a file or section has many hard mandates, absolute words, global scope, few exceptions, repeated rules, contradiction density, or rigid tool instructions. Prefer section-level recommendations when one section is the problem; prefer file-level recommendations when the entire file acts like a policy bundle.

## Remediation Types

- `COMPRESS_PROMPT`: shorten long durable prompts while preserving intent.
- `MOVE_TO_SKILL`: move reusable procedure into a skill.
- `MOVE_TO_CONFIG`: move runtime limits or tool settings into config.
- `MOVE_TO_MEMORY`: store durable factual preferences, not procedures or tasks.
- `MOVE_TO_PROJECT_AGENTS`: move project-specific behavior to a project instruction file.
- `DELETE_DUPLICATE`: remove repeated guidance after confirming the canonical source.
- `REWRITE_CONTRADICTION`: replace conflicting rules with a scoped policy.
- `SOFTEN_OVER_ENFORCED_RULE`: turn a global hard rule into a contextual preference.
- `ADD_EXCEPTION`: add explicit exceptions to avoid brittle behavior.
- `ADD_GUARDRAIL`: add missing safety, trust-boundary, or secret-handling policy.
- `ISOLATE_UNTRUSTED_TEXT`: quote, sandbox, or mark untrusted prompt-like content.
- `REPLACE_COUNTERPRODUCTIVE_WORKFLOW`: replace a harmful workflow with a structural or search-first workflow.
- `CLARIFY_SCOPE`: specify actor, layer, file scope, or trigger conditions.
- `SPLIT_FILE`: separate identity, workflow, config, memory, examples, and reports.
- `ARCHIVE_STALE_SECTION`: move historical or obsolete material out of active prompts.

## Smart File-Inspection Policy

Recommend this pattern when a framework has brittle file-reading rules:

```markdown
When inspecting files, first determine relevance and structure. Use file inventory, headings, symbols, search results, and targeted ranges. Avoid arbitrary tiny chunks unless debugging a known location. Read full files when they are small or when full context is necessary. For large files, read semantically meaningful sections rather than fixed-size fragments.
```