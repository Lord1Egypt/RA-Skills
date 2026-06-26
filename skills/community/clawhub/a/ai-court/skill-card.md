## Description: <br>
AI 朝廷 is an OpenClaw-based multi-agent collaboration skill that provides Ming, Tang, and modern enterprise role templates with 1-11 bot configurations for Feishu and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanikua](https://clawhub.ai/user/wanikua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team administrators use this skill to deploy an OpenClaw multi-agent team with predefined coordination roles, routing templates, and platform setup guidance. It supports personal, small-team, and larger team configurations across Feishu and Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default templates can expose powerful multi-agent bots too broadly. <br>
Mitigation: Restrict allowed users, servers, channels, and direct messages, and remove broad mention triggers before deployment. <br>
Risk: Bot tokens, Feishu app IDs, app secrets, and optional API tokens are required for deployment. <br>
Mitigation: Keep secrets outside shared configuration files, validate every binding, and rotate credentials if a configuration is exposed. <br>
Risk: Copying templates into an existing OpenClaw configuration can overwrite working settings or apply unsuitable sandbox permissions. <br>
Mitigation: Back up the existing OpenClaw config first and align sandbox permissions with each role before restarting the gateway. <br>
Risk: Archived records or multi-agent conversation logs may retain sensitive user or business content. <br>
Mitigation: Define retention and redaction rules for archived records before enabling the system for real users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanikua/ai-court) <br>
- [Feishu Quick Setup Guide](artifact/docs/feishu-setup-simple.md) <br>
- [Feishu Flexible Configuration Guide](artifact/docs/feishu-flexible-setup.md) <br>
- [Docker Image Configuration Guide](artifact/references/docker-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw setup guidance, role templates, routing configuration, and deployment commands.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and artifact _meta.json; artifact SKILL.md and package.json list 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
