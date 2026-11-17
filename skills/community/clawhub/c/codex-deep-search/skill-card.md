## Description:

Deep web search using Codex CLI for complex queries that need multi-source synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwzh](https://clawhub.ai/user/jiangwzh)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when ordinary web search snippets are insufficient and a query needs deeper multi-source research, cross-referencing, and a written search report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous writable searches may modify files or produce untrusted research output.

Mitigation: Run only after review, restrict output to a dedicated results directory, and avoid full-auto workspace-write execution for untrusted prompts.

Risk: Telegram delivery can send research content outside the local workspace.

Mitigation: Use non-sensitive queries and remove or explicitly configure Telegram delivery before use.

Risk: The local OpenClaw wake callback is undocumented in the public skill description.

Mitigation: Disable the wake-hook behavior unless the local endpoint, token handling, and intended callback behavior have been reviewed.

## Reference(s):

- [Codex Deep Search ClawHub page](https://clawhub.ai/jiangwzh/skills/codex-deep-search)
- [Publisher profile](https://clawhub.ai/user/jiangwzh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown search report with task metadata and optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write incremental result files and status metadata; may send an optional Telegram callback when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
