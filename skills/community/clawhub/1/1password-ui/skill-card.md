## Description: <br>
1Password UI tab for OpenClaw dashboard. Manage secrets, credential mappings, and auth state from the Control UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add a 1Password tab to the OpenClaw dashboard, browse vault metadata, manage credential mappings, and support skill access to secrets through 1Password CLI or Connect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill adds gateway RPC methods that can read secrets from 1Password. <br>
Mitigation: Restrict gateway access to trusted local callers or authenticated networks, require user-controlled 1Password authentication, and use least-privilege 1Password Connect tokens. <br>
Risk: Server security evidence reports an artifact-backed command-injection risk in the backend. <br>
Mitigation: Review or patch the backend before installation, replacing shell-string execution with spawn or execFile-style argument handling. <br>
Risk: RPC responses, command stdout, logs, Connect tokens, and mapping files may expose sensitive credential context. <br>
Mitigation: Treat these outputs and files as sensitive, avoid exposing them to untrusted users, and keep mapping files permissioned for the owner only. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/1password-ui) <br>
- [Installation Instructions](INSTALL_INSTRUCTIONS.md) <br>
- [1Password CLI Documentation](https://developer.1password.com/docs/cli) <br>
- [1Password Connect Documentation](https://developer.1password.com/docs/connect) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and Python reference code plus shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw gateway and UI integration steps, 1Password CLI or Connect configuration, and secret-mapping guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
