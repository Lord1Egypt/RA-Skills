## Description: <br>
OpenClaw plugin and skill hybrid that adds long-term memory, anti-hallucination checks, self-evolution routines, workflow orchestration, maintenance jobs, auto-scan, and version checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grushheart](https://clawhub.ai/user/grushheart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to extend an agent with persistent memory, retrieval, workflow routing, quality checks, scheduled maintenance, and workspace scans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runs local commands and Python engines from OpenClaw lifecycle hooks. <br>
Mitigation: Review the package before installation and test in a separate OpenClaw workspace where local command execution is acceptable. <br>
Risk: Modifies workspace state, memory, skills, and agent behavior rules. <br>
Mitigation: Back up workspace data and avoid installing in environments that contain sensitive memory or configuration data. <br>
Risk: Registers or replaces OpenClaw scheduled jobs. <br>
Mitigation: Inspect existing cron tasks before installation and verify scheduled jobs after installation. <br>
Risk: Contacts clawhub.ai for version checks. <br>
Mitigation: Install only in environments where outbound version-check traffic to ClawHub is permitted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/grushheart/crusheart-performance-autobrain) <br>
- [README](artifact/README.md) <br>
- [Architecture Reference](artifact/bundle/ARCHITECTURE.md) <br>
- [Install Guide](artifact/bundle/INSTALL_GUIDE.md) <br>
- [Plugin Manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text responses with command and configuration snippets when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local workspace state, schedule OpenClaw jobs, scan memory and skill directories, and check clawhub.ai for version updates.] <br>

## Skill Version(s): <br>
6.3.1 (source: package.json, server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
