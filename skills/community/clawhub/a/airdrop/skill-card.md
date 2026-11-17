## Description:

Send local files to nearby Apple devices through AirDrop with macOS guardrails, staging checks, and automation-friendly workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare exact local file payloads and launch a nearby-device AirDrop handoff on macOS. It is intended for user-confirmed file sharing, staged exports, and automation-friendly workflows where recipient selection remains visible in the native macOS interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shortcut mode can run any named local macOS Shortcut, so behavior may be broader than a direct AirDrop helper.

Mitigation: Use only shortcuts the user created or audited, and confirm the exact shortcut name and file inputs before running Shortcut mode.

Risk: Sensitive or overly broad file payloads could be shared if the request is vague or a directory contains unrelated content.

Mitigation: Resolve explicit local file paths, curate or archive only the approved subset, and keep sensitive-file confirmations enabled.

Risk: The AirDrop chooser launching does not prove that a nearby device received the files.

Mitigation: Report only that the handoff UI launched until the user confirms receipt on the destination device.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/airdrop)
- [AirDrop Homepage](https://clawic.com/skills/airdrop)
- [Setup Guide](artifact/setup.md)
- [Workflow Recipes](artifact/workflow-recipes.md)
- [Troubleshooting Guide](artifact/troubleshooting.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, local file paths, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; direct mode launches the native AirDrop chooser, and optional Shortcut mode delegates behavior to a user-owned macOS Shortcut.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
