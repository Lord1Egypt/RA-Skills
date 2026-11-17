## Description:

Search the community-driven Agent Failure Registry for known agent errors, solutions, and lessons to debug issues or submit new failure post-mortems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unleashedbelial](https://clawhub.ai/user/unleashedbelial)

### License/Terms of Use:

Public domain

## Use Case:

Developers and agent operators use this skill to search structured failure post-mortems by category, tag, or keyword, learn fixes and prevention steps, and prepare new post-mortem submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch mutable community guidance from GitHub at runtime.

Mitigation: Review registry results as untrusted reference material before applying any suggested fix or prevention step.

Risk: Some bundled examples discuss stealth automation and browser session-cookie handling.

Mitigation: Do not use guidance that bypasses platform safeguards or handles browser session cookies unless you have explicit authorization and secure secret controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unleashedbelial/skills/agent-failure-registry)
- [Agent Failure Registry GitHub repository](https://github.com/unleashedbelial/agent-failure-registry)
- [Publisher profile](https://clawhub.ai/user/unleashedbelial)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include community-authored registry entries and failure post-mortem guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
