## Description:

Upload files to Govilo and generate unlock links via Bot API for ZIP files, folders, or individual files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hau823823](https://clawhub.ai/user/hau823823)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to package digital files, upload them to Govilo storage, and create paid unlock links through the Govilo Bot API. It helps agents guide configuration and run the create-link workflow with user-provided product details, API credentials, and seller wallet address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include remote installer commands for uv, which can execute code retrieved over the network.

Mitigation: Use Homebrew or another trusted package manager for uv when available, and review installer sources before running them.

Risk: Using a shared environment file can expose unrelated secrets during command execution.

Mitigation: Use a dedicated .env.govilo file containing only GOVILO_API_KEY and, if needed, SELLER_ADDRESS.

Risk: Packaging untrusted directories or extracted archives can upload files the user did not intend to share.

Mitigation: Upload only directories the user created or has inspected, and avoid untrusted repositories or archives until symlink handling and temporary-file creation are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hau823823/skills/gen-paylink-govilo)
- [Publisher Profile](https://clawhub.ai/user/hau823823)
- [Clawdis Homepage](https://github.com/hau823823/gen-paylink-govilo)
- [Bot API Quick Reference](references/bot-api-quick-ref.md)
- [Setup Guide](references/setup-guide.md)
- [Govilo](https://govilo.xyz/)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOVILO_API_KEY and SELLER_ADDRESS or an address argument; uploads are limited to ZIP packages of 20 MB and 20 files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
