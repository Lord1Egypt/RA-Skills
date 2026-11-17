## Description:

无头浏览器自动化CLI,支持可访问性树快照与确定性元素选择,适合个人开发者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to drive a headless browser CLI for navigation, ref-based interaction, page inspection, screenshots, PDFs, and session state workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation scope is broad enough that an agent may invoke browser automation for unrelated coding or deployment requests.

Mitigation: Use the skill only for explicit browser automation tasks and keep it disabled or out of scope for general development assistance.

Risk: Saved browser state files such as auth.json, admin-auth.json, or user-auth.json may contain login state that can grant account access.

Mitigation: Treat browser state files as secrets: do not commit, share, or reuse them across accounts, and store them only where secret handling is appropriate.

Risk: The skill depends on installing and running a global npm browser CLI with native browser tooling.

Mitigation: Install the CLI only from a trusted package source and use it in environments where global browser automation tooling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/browser-agent-tool-free)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser state files, screenshots, PDFs, and extracted page data depending on the invoked CLI command.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
