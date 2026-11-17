## Description:

Guides agents through installing and configuring lark-cli for Feishu/Lark, including environment checks, npm installation, app credential setup, OAuth login handoff, verification, and first commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent guide Feishu/Lark CLI setup, prompting for local commands and browser-based OAuth or configuration steps the user must complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks agents to install unpinned global packages and globally added skills.

Mitigation: Prefer pinned package versions, avoid sudo npm install, and review the exact globally added skills before activation.

Risk: The setup flow handles Feishu App Secrets and authenticates lark-cli under the user's Feishu/Lark identity.

Mitigation: Enter secrets only into the local CLI prompt, do not share app credentials, and use dry-run checks before commands with side effects.

Risk: Generated commands can include user-provided domain values.

Mitigation: Validate domain values before execution and treat commands containing unvalidated domains as unsafe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/feishu-cli-setup)
- [larksuite/cli repository](https://github.com/larksuite/cli)
- [Feishu Open Platform app console](https://open.feishu.cn/app)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with shell commands and user handoff prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-completed browser authorization and local credential entry for Feishu/Lark setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
