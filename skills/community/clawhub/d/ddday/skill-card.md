## Description: <br>
ddday is a daily work journal and machine migration toolkit that scans registered projects, generates daily dashboards, and provides one-command data export and restore for machine migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual operators use ddday to record project activity, generate AI-readable work context, and migrate local work state between machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration and snapshot modes can collect credentials, .env material, AI memory, environment details, and business context into portable files. <br>
Mitigation: Review and narrow packaged paths before use, exclude sensitive material unless deliberately required, and inspect generated archives before sharing or restoring. <br>
Risk: Generated restore scripts and cron entries can modify a new machine's environment. <br>
Mitigation: Inspect setup.sh and cron changes before execution, then run the health check after restore. <br>
Risk: Migration archives may contain sensitive local work context. <br>
Mitigation: Store migration archives in encrypted locations and avoid transmitting them through untrusted channels. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cosmofang/ddday) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code, shell commands, JSON configuration, and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate daily logs, dashboard HTML, context snapshots, migration archives, manifests, setup scripts, and health-check reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
