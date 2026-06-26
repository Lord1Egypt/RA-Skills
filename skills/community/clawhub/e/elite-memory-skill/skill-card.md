## Description: <br>
A memory-management skill for AI agents that maintains daily and long-term Markdown memories, supports write-ahead logging practices, syncs memory files to GitHub, and can send Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renguanjie](https://clawhub.ai/user/renguanjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain durable AI memory across sessions, organize daily and long-term notes, and automate scheduled sync and review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The GitHub sync workflow can commit and push the whole OpenClaw workspace instead of only memory files. <br>
Mitigation: Review the sync script before enabling cron, narrow git add -A to an allowlist such as MEMORY.md, SESSION-STATE.md, and memory/, and verify the memory remote points to a private repository you control. <br>
Risk: Feishu notifications may send sync metadata outside the local workspace when FEISHU_USER_ID is configured. <br>
Mitigation: Set FEISHU_USER_ID only when Feishu notifications are intended and acceptable for the memory workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renguanjie/elite-memory-skill) <br>
- [AI Memory GitHub Repository](https://github.com/renguanjie/ai-memory) <br>
- [OpenClaw Memory Documentation](https://docs.openclaw.ai/memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local Markdown memory files, shell-based automation steps, Git sync commands, and optional Feishu notification configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
