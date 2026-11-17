## Description:

让AI代理控制浏览器自动化网页操作。支持 Claude/GPT/Gemini/Ollama，可执行填表、购物、搜索等任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill for guidance on installing, configuring, and using browser-use so AI agents can automate browser tasks such as form filling, shopping workflows, web searches, screenshots, and authenticated site interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote installers and package commands.

Mitigation: Use pinned package versions and commit-specific URLs, inspect downloaded scripts before running them, and avoid curl-to-shell execution.

Risk: Browser automation can act on authenticated sessions, synced profiles, forms, uploads, purchases, email, and account state.

Mitigation: Use a dedicated browser profile and require manual confirmation before purchases, form submissions, uploads, email sending, or account changes.

Risk: The release is flagged suspicious because authentication and browser profile sharing are not scoped enough.

Mitigation: Review the skill before installation and do not sync or reuse a personal browser profile unless the shared authentication data is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smseow001/skills/browser-use-guide)
- [browser-use GitHub repository](https://github.com/browser-use/browser-use)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python snippets, configuration examples, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser automation setup guidance, API key configuration notes, CLI examples, and integration instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
