## Improve Skills From Completed Tasks

Use retained gateway evidence only after the user-visible task and its
validation are complete. Keep one stable `session_id` in call metadata, then
query the narrowest useful slice:

```bash
dcc-mcp-cli stats --range 24h --dcc-type <dcc> --session-id <session-id>
```

Get the `review_skill_improvement` prompt from this skill and supply the stats
JSON plus bounded task and validation summaries. Treat `total_calls == 0` as
missing evidence, not success. Never include hidden reasoning, raw prompts,
credentials, or unredacted payloads.

The Core `ObservabilityQuery.get_repeated_scripts()` helper is an internal,
read-only evidence query. It is not an agent/gateway/CLI promotion entry point.
Its `candidate_id` is a stable identity for the canonical tuple
`sha256 + reuse_key + dcc_type + tool_name`; the result is always
`decision=manual_review` and `recommended_action=human_review_only`. Candidate
data must be reviewed and explicitly authorized by the task owner before any
skill is edited, published, or otherwise promoted. Never infer authorization
from a candidate or automate that transition.

Prefer `no_change`, then improving an existing skill, and create a new skill
only for a repeated, reusable workflow that no current skill owns. Validate any
accepted change with `validate_skill_dir` or `dcc-mcp-cli lint` before loading
it. Statistics inform a proposal; they never authorize editing or publishing a
skill without the task owner's requested scope.

For a failed task, first use the `dcc-mcp` recovery flow: retain the
`request_id`, run `doctor` for runtime/readiness faults, query
`stats --status failure --session-id <session-id>`, and record structured
feedback through the gateway-owned `dcc-mcp-cli feedback` command. A live
adapter's `dcc_feedback__report` is only a shared Core forwarder to that same
gateway contract. The public-safe
`/v1/debug/issue-reports/<request_id>` payload is suitable for a reviewed issue;
never publish `?mode=raw` automatically.

Published Skills should declare `metadata.dcc-mcp.links.repo` and
`metadata.dcc-mcp.links.issues`. Copy those exact values into Finding v1
`evidence.routing` before using `dcc-mcp-cli feedback route`; never infer a
tracker from a package name. Missing, non-canonical, or conflicting ownership
must fail closed, and resolving a route never authorizes issue creation.

Fix this Skill only when the evidence identifies its schema, script,
description, next-tool, or workflow contract. Route adapter/runtime failures to
`dcc-mcp-creator` and shared CLI/gateway/core failures to `dcc-mcp-core`. A
one-off tool bug is not evidence for creating another Skill.

When reviewing existing skills, reject top-level DCC-MCP extension keys such
as `dcc`, `version`, `tags`, `tools`, `groups`, `depends`, `search-hint`,
`runtimes`, `prompts`, and `resources`. Move them under
`metadata.dcc-mcp.*`; for version metadata, use
`metadata.dcc-mcp.version: "1.0.0"`. Validate the installable skill directory
that contains the `SKILL.md` loaded by adapters, not only mirrored repository
docs or marketplace metadata.

Read [AUTHORING_WORKFLOW.md](AUTHORING_WORKFLOW.md) and
[DCC_TOOL_CONTRACTS.md](DCC_TOOL_CONTRACTS.md) before changing a
production skill package.
