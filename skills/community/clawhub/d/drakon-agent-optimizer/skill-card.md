## Description: <br>
CLI tool that audits OpenClaw configuration files for misconfigurations, token waste, security issues, and stale authentication while reading local JSON configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and run an auditing CLI that reviews local OpenClaw configuration, authentication profile freshness, model settings, workspace security patterns, token efficiency, and paid fleet checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external npm package. <br>
Mitigation: Install only if you trust the Drakon Systems package and review the package source and npm metadata before use. <br>
Risk: Optimization or fix modes may modify local OpenClaw configuration files. <br>
Mitigation: Start with audit or dry-run modes, review proposed changes, and rely on the tool's backup behavior before applying fixes. <br>
Risk: Fleet SSH audit reads OpenClaw configuration from remote hosts through existing SSH configuration. <br>
Mitigation: Use fleet mode only for hosts you intend to query and confirm that your SSH configuration targets the expected machines. <br>
Risk: Local snapshots may contain sensitive configuration details. <br>
Mitigation: Protect access to the local snapshot directory and remove snapshots that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jarvis-drakon/drakon-agent-optimizer) <br>
- [Drakon Systems product page](https://drakonsystems.com/products/agent-optimizer) <br>
- [npm package](https://www.npmjs.com/package/@drakon-systems/agent-optimizer) <br>
- [Source repository](https://github.com/Drakon-Systems-Ltd/agent-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/jarvis-drakon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audit findings, dry-run recommendations, install commands, and fix guidance; paid modes may modify local files after creating backups.] <br>

## Skill Version(s): <br>
0.8.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
