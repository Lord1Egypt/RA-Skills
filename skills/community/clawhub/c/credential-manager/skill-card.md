## Description: <br>
Consolidates scattered OpenClaw API keys and credentials into a centralized `~/.openclaw/.env` file with scanning, backup, permission hardening, validation, enforcement, and cleanup helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Callmedas69](https://clawhub.ai/user/Callmedas69) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to migrate scattered OpenClaw credentials into one protected `.env` file and enforce that credential standard before running other skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad authority over local secrets and persistent plaintext credential files. <br>
Mitigation: Install and run it only when credential centralization into `~/.openclaw/.env` is intended; review every discovered path before consolidation. <br>
Risk: Automated consolidation can import unrelated application secrets or wallet seed phrases. <br>
Mitigation: Run the scan first, inspect the proposed inputs, and avoid auto-confirm mode until the exact changes are understood. <br>
Risk: Backups and cleanup can preserve, expose, or remove sensitive credential files. <br>
Mitigation: Verify or restrict backup permissions, test the new `.env`, confirm rollback works, and run cleanup only after validation. <br>


## Reference(s): <br>
- [Credential Manager on ClawHub](https://clawhub.ai/Callmedas69/credential-manager) <br>
- [Security Best Practices](references/security.md) <br>
- [Supported Services](references/supported-services.md) <br>
- [Consolidation Rule](CONSOLIDATION-RULE.md) <br>
- [Core Principle](CORE-PRINCIPLE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update `.env`, `.env.example`, `.gitignore`, timestamped backups, and validation reports when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.3.0 (source: server evidence and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
