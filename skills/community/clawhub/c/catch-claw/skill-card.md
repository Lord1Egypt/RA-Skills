## Description: <br>
Search, install, and export agentars from the CatchClaw marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lovelcp](https://clawhub.ai/user/Lovelcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search the CatchClaw marketplace, install selected agentar packages into OpenClaw workspaces, export existing agents as distributable ZIP packages, and restore workspace backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that a crafted new-agent name can cause file writes outside the advertised workspace area. <br>
Mitigation: Install only trusted agentars, use simple new-agent names containing letters, numbers, hyphens, or underscores, and avoid names containing slashes or dots. <br>
Risk: Overwrite and rollback operations replace workspace contents. <br>
Mitigation: Require explicit user selection before overwrite or rollback, and review the backup path before continuing. <br>
Risk: Passing an API key during install writes credentials into the installed workspace. <br>
Mitigation: Pass API keys only when the selected agentar truly requires them and review the installed workspace before sharing or exporting it. <br>


## Reference(s): <br>
- [CatchClaw ClawHub listing](https://clawhub.ai/Lovelcp/catch-claw) <br>
- [CatchClaw homepage](https://github.com/OpenAgentar/catchclaw) <br>
- [CatchClaw registry](https://catchclaw.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or replace local workspace files, write optional credentials, and export agentar ZIP packages through the bundled CLI.] <br>

## Skill Version(s): <br>
3.5.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
