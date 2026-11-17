## Description:

Reduces Claude API token consumption and tracks spending by diagnosing waste patterns, recommending optimizations, and generating cost reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicope](https://clawhub.ai/user/nicope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Token Saver to audit Claude API usage, identify cost waste in OpenClaw configs and prompt context, and produce prioritized savings recommendations or cost reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use ANTHROPIC_API_KEY to query Anthropic usage data.

Mitigation: Provide the API key only when usage reporting is intended and remove it from the environment when not needed.

Risk: The skill may inspect local OpenClaw prompt and config files and propose configuration changes.

Mitigation: Review the shown diff and approve only expected edits before allowing any file changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicope/skills/clawtrix-token-saver)
- [Anthropic usage API endpoint](https://api.anthropic.com/v1/usage?days=7)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and optional JSON from the cost report script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Anthropic usage API with ANTHROPIC_API_KEY; proposed configuration edits require user confirmation after a diff.]

## Skill Version(s):

0.1.0 (source: server release metadata, target metadata, artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
