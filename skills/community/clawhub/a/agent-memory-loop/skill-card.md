## Description: <br>
Lightweight self-improvement loop for AI agents that captures errors, corrections, and discoveries in one-line Markdown logs, deduplicates them, and queues recurring or critical lessons for human-approved promotion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give reset-prone agents a lightweight memory loop for logging mistakes, corrections, discoveries, and desired capabilities. It supports pre-task review and human-approved promotion of recurring or critical lessons into project instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture secrets or sensitive private data. <br>
Mitigation: Install the skill only in workspaces where persistent agent memory is intended, and avoid logging secrets or sensitive private data. <br>
Risk: Promoting logged entries into instruction files could introduce incorrect or misleading guidance. <br>
Mitigation: Review .learnings/promotion-queue.md before copying any rule into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or similar files. <br>
Risk: External content could be treated as a trusted lesson if source boundaries are ignored. <br>
Mitigation: Use source labels and do not promote source:external entries unless independently verified and re-logged with fresh evidence. <br>


## Reference(s): <br>
- [Agent Memory Loop on ClawHub](https://clawhub.ai/zurbrick/agent-memory-loop) <br>
- [ClawHub package homepage](https://clawhub.ai/agent-memory-loop) <br>
- [Repository link from OpenClaw metadata](https://github.com/donzurbrick/agent-memory-loop) <br>
- [Logging Format Reference](references/logging-format.md) <br>
- [Operating Rules Reference](references/operating-rules.md) <br>
- [Promotion Queue Format Reference](references/promotion-queue-format.md) <br>
- [Detail File Template](references/detail-template.md) <br>
- [Design Tradeoffs](references/design-tradeoffs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local .learnings Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reviews workspace-local .learnings files; requires grep and date.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
