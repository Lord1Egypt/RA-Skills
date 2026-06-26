## Description: <br>
Scans an OpenClaw environment for leaked API keys, tokens, credentials in .env files, installed skills, and shell history, and offers permissioned fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukiraman](https://clawhub.ai/user/sukiraman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Canary to audit local workspaces and configuration files for exposed credentials, understand findings in plain language, and apply or receive guided fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad credential-audit behavior can inspect sensitive local files and paths. <br>
Mitigation: Review the paths Canary will inspect before deep scans and avoid pasting real secrets into chat. <br>
Risk: Fixes and backup behavior can change files or leave .canary state, backups, and an integrity marker after use. <br>
Mitigation: Approve fixes one by one, review retained state locations, and remove Canary state when it is no longer needed. <br>
Risk: Heuristic secret detection can produce false positives or findings that require human judgment. <br>
Mitigation: Review each finding before changing files or rotating credentials, and rotate credentials when a real exposure is confirmed. <br>


## Reference(s): <br>
- [Canary ClawHub release](https://clawhub.ai/sukiraman/canary) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Claude Project setup guide](artifact/claude-project/project-instructions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain-language Markdown reports with inline shell commands and fix instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file permission changes, backups, scan-state updates, and credential-rotation guidance; user approval is expected before fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
