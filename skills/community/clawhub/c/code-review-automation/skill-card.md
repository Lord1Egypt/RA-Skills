## Description:

Automates GitHub pull request review with Claude LLM analysis, security scanning, code quality scoring, and style checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect GitHub pull requests, summarize file changes, run AI-assisted review, and surface security or style issues before merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An overly broad GitHub token can expose repository data beyond the pull requests being reviewed.

Mitigation: Use a fine-grained GitHub token limited to the specific repositories and read-only contents, metadata, and pull request permissions needed.

Risk: Untrusted pull request content is sent to the LLM and can influence generated review, quality score, or merge guidance.

Mitigation: Treat LLM output as advisory, keep human review in the loop, and rely on deterministic checks independently of the generated recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirofumiko/skills/code-review-automation)
- [Anthropic Console](https://console.anthropic.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown review output with optional configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub token; Claude analysis requires an Anthropic API key.]

## Skill Version(s):

1.0.2 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
