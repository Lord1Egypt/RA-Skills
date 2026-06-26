## Description: <br>
Auto Authenticator Local helps authorized users store TOTP seeds in local secure credential stores and generate explicit, on-demand 6-digit codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucasZH7](https://clawhub.ai/user/LucasZH7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and authorized operators use this skill to manage local TOTP aliases for accounts they own or are explicitly authorized to access. It supports secure local setup, deletion, and one-at-a-time code generation without cloud synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real TOTP seeds passed directly on the command line may be exposed through shell history or process listings. <br>
Mitigation: Do not pass production seeds through shell commands for this version; use only inspected local workflows and rotate any seed that may have been exposed. <br>
Risk: The one-line installer retrieves and executes remote code and installs Python dependencies. <br>
Mitigation: Clone or download a pinned release, inspect the installer before running it, and install dependencies in a virtual environment with pinned versions. <br>
Risk: The skill stores MFA seeds in the local operating system credential store, so device or local account compromise can affect those accounts. <br>
Mitigation: Use the skill only on trusted devices with appropriate OS credential-store protections, and delete or rotate aliases when access changes. <br>


## Reference(s): <br>
- [Security notes for local TOTP workflows](references/security.md) <br>
- [ClawHub skill page](https://clawhub.ai/LucasZH7/auto-authenticator-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts can emit plain text or JSON for alias-scoped TOTP results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one alias-scoped TOTP response at a time and does not support bulk secret export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
