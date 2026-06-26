## Description: <br>
Credential Manager scans for scattered API keys and credential files, backs them up, consolidates them into a protected OpenClaw .env file, and validates permissions and git protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxz9909](https://clawhub.ai/user/cxz9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local credential sprawl, migrate supported service credentials into a single secured OpenClaw .env file, and enforce credential-loading expectations for other skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad authority over sensitive secrets, including scanning, copying, centralizing, and deleting credential files. <br>
Mitigation: Run scan-only first, review every detected path, avoid --yes and cleanup until the migration plan is reviewed, and verify backups before deleting old files. <br>
Risk: Centralizing credentials into a plaintext .env file creates a high-value local secret store. <br>
Mitigation: Keep the file at mode 600, ensure it is git-ignored, encrypt backups, and use an encrypted secret manager for high-value credentials such as wallet seed phrases or private keys unless plaintext storage is explicitly accepted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cxz9909/cxz9909-credential-manager) <br>
- [Core Principle: Centralized Credential Management](CORE-PRINCIPLE.md) <br>
- [Credential Consolidation Rule](CONSOLIDATION-RULE.md) <br>
- [Security Best Practices](references/security.md) <br>
- [Supported Services](references/supported-services.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local credential files, backups, .gitignore, and .env.example when the described scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata and docs mention 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
