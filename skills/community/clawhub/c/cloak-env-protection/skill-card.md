## Description: <br>
Protect .env secrets from AI agents. Real credentials encrypted in a vault — agents see structurally valid sandbox values on disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danieltamas](https://clawhub.ai/user/danieltamas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to recognize Cloak-protected projects, avoid exposing real .env secrets, and use Cloak commands for secret-aware workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes remote installer commands that fetch and execute scripts. <br>
Mitigation: Inspect the installer first and verify its source or checksum/signature when available before running it on machines with sensitive files or credentials. <br>
Risk: Incorrect handling of a Cloak-protected project could expose or overwrite secret-management state. <br>
Mitigation: Use Cloak commands such as `cloak run`, `cloak set`, and `cloak edit`; do not read vault, recovery, or Cloak config files, and do not directly edit `.env` when `.cloak` is present. <br>


## Reference(s): <br>
- [Cloak skill listing](https://clawhub.ai/danieltamas/cloak-env-protection) <br>
- [Cloak installer for macOS and Linux](https://getcloak.dev/install.sh) <br>
- [Cloak installer for Windows](https://getcloak.dev/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing instructions for Cloak detection, .env handling, command use, and recovery guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
