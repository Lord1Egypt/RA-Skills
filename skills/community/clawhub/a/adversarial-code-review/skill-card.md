## Description:

Use when reviewing pull requests or critiquing code changes and you want high-signal, low-noise feedback by running multiple adversarial agents that challenge each other's findings. Works standalone or integrated into CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reikys](https://clawhub.ai/user/reikys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run adversarial, multi-agent review of pull requests, code changes, and longer design plans. It helps filter automated review output down to a few high-confidence, high-priority, actionable findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs may be sent to Anthropic through Claude CLI.

Mitigation: Use only on repositories and diffs that can be shared with that provider; avoid secrets, regulated data, and code with sharing restrictions.

Risk: CI examples use an API key and can optionally post automated review comments to GitHub.

Mitigation: Protect the Anthropic API key, use least-privilege GitHub permissions, and review CI behavior before enabling PR comments.

Risk: Automated code-review findings may be incorrect, incomplete, or overly confident.

Mitigation: Keep a human reviewer in the loop, especially for security-critical or compliance-gated changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review output is intended to contain only a small number of high-confidence, high-priority comments with location, impact, suggested fix, confidence, and priority.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
