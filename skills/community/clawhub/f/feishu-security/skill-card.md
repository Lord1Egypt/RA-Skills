## Description: <br>
Helps an OpenClaw Feishu bot isolate group-chat access by binding a privileged owner, requiring approval for skill installs, segmenting permissions, filtering prompt injection attempts, and protecting sensitive paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carolyn0719](https://clawhub.ai/user/carolyn0719) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators and Feishu bot administrators use this skill to keep group-chat interactions in a safer, lower-privilege mode while preserving owner-only private-chat control for sensitive actions such as file changes, command execution, and skill installation approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Feishu owner receives full local-agent control, including approvals for file changes, command execution, and skill installations. <br>
Mitigation: Before installing or enabling the skill, confirm that ~/.openclaw/openclaw.json or FEISHU_OWNER_ID identifies the intended owner, or bind the owner manually in a private deployment. <br>
Risk: If the skill remains unbound after installation, the first private-chat binding flow can determine the owner. <br>
Mitigation: Complete owner binding during setup, verify the bound owner with the provided verification flow, and treat unexpected unbound state as a deployment issue. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carolyn0719/feishu-security) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [config.json](artifact/config.json) <br>
- [verify.sh](artifact/verify.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes owner-binding, approval, permission, logging, and verification guidance for Feishu bot deployments.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata; artifact frontmatter reports 2.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
