## Description: <br>
Install and configure EverOS for OpenClaw natural-language memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alwaysday1](https://clawhub.ai/user/alwaysday1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure the EverOS context-engine plugin so conversations can recall and save persistent memory through a self-hosted EverOS backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content may be stored by the configured EverOS backend and may appear in logs. <br>
Mitigation: Use only a trusted backend, verify the backend URL before use, and avoid sensitive conversations until logging and retention behavior are understood. <br>
Risk: The installer persistently changes OpenClaw memory configuration. <br>
Mitigation: Review ~/.openclaw/openclaw.json before and after installation and keep the generated backup for rollback. <br>
Risk: External setup commands can install or run additional components. <br>
Mitigation: Prefer pinned or inspected setup commands and confirm the backend source before running installers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alwaysday1/evermind-ai-everos) <br>
- [Publisher profile](https://clawhub.ai/user/alwaysday1) <br>
- [EverMemOS backend](https://github.com/EverMind-AI/EverMemOS) <br>
- [Artifact README](artifact/README.md) <br>
- [Plugin metadata](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation, OpenClaw configuration, backend health checks, restart, and natural-language verification.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
