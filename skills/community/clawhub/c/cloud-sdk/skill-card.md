## Description:

Cloud Sdk provides a local shell-based workflow helper for project initialization, checks, builds, tests, deployment guidance, configuration, templates, documentation, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to invoke or reason about a local CLI-style project workflow helper for common lifecycle tasks such as setup, quality checks, builds, tests, deployment checklists, configuration, documentation, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package name and metadata frame it as the Go Cloud Development Kit, while the security evidence says it behaves like a local shell-based workflow helper.

Mitigation: Review the skill identity before installation and treat it as a local workflow helper unless separate trusted evidence confirms Go Cloud Development Kit behavior.

Risk: The skill keeps persistent command history, which may capture sensitive paths or arguments.

Mitigation: Avoid passing secrets or sensitive paths as command arguments, set CLOUD_SDK_DIR to a controlled location during testing, and clear history logs when appropriate.

## Reference(s):

- [Cloud Sdk on ClawHub](https://clawhub.ai/xueyetianya/skills/cloud-sdk)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local command history and configuration under CLOUD_SDK_DIR or the user's XDG data directory.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
