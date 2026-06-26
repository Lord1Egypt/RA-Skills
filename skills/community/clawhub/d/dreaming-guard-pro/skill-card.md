## Description: <br>
Dreaming Guard Pro provides smart prevention and auto-recovery for OpenClaw dreaming context overflow by monitoring growth trends, archiving intelligently, compressing context, protecting process memory, and self-healing after crashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuangzhanzhiwang](https://clawhub.ai/user/kuangzhanzhiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to monitor dreaming context growth, generate health reports, and apply archiving, compression, and recovery workflows before context storage or memory pressure causes disruption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite, archive, restore, and retain local context data. <br>
Mitigation: Start with read-only health reports, explicitly configure watched paths, and keep separate backups before enabling automated actions. <br>
Risk: Lossy or aggressive compression may remove context that a user expected to preserve. <br>
Mitigation: Use lossless compression first and enable lossy or aggressive modes only when context loss is acceptable. <br>
Risk: Daemon or cron automation can run file operations repeatedly without direct review. <br>
Mitigation: Do not enable daemon or cron mode until overwrite, restore, retention, and log/report exposure are reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kuangzhanzhiwang/dreaming-guard-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/kuangzhanzhiwang) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, JSON, code, shell commands, configuration] <br>
**Output Format:** [Markdown, plain text, JSON reports, JavaScript API usage, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates health reports and can provide operational commands or configuration for monitoring, archiving, compression, and recovery.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
