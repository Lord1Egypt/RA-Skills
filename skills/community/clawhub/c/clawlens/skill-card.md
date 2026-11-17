## Description:

Clawlens analyzes OpenClaw conversation history to surface usage patterns, friction points, and skill effectiveness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunzhang](https://clawhub.ai/user/dunzhang)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to review their conversation history, identify common task patterns, inspect friction points, and generate a usage insights report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history, including possible tool-output excerpts, may be sent to the selected external LLM provider.

Mitigation: Use the shortest practical --days window, choose the provider deliberately, and review the report inputs before sharing results.

Risk: Auto-detection reads OpenClaw provider configuration and stored credentials.

Mitigation: Review OpenClaw provider configuration before using auto-detect, or specify a model explicitly with the corresponding environment variable.

Risk: HTML reports generated from session content may expose untrusted content in a browser.

Mitigation: Prefer Markdown output for untrusted session content and only open HTML reports from trusted local runs.

## Reference(s):

- [Clawlens Report Format Reference](references/report-format.md)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

## Skill Output:

**Output Type(s):** [text, markdown, html]

**Output Format:** [Markdown report by default, with optional self-contained HTML output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report language can be Chinese or English; the default analysis window is 180 days.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
