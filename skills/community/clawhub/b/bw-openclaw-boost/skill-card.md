## Description: <br>
OpenClaw Boost enhances OpenClaw efficiency with cost tracking, memory management, compression, permission control, and task coordination tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bw520333](https://clawhub.ai/user/bw520333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor local agent cost, token budget, memory relevance, compaction status, permission checks, and task coordination from local shell tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The permission manager can mark risky command execution patterns as safe. <br>
Mitigation: Review and tighten permission defaults before wiring the checker into OpenClaw auto-approval; keep broad write, network, and execute patterns in ask mode. <br>
Risk: Local memory and logging features may retain sensitive task details if users store them there. <br>
Mitigation: Avoid storing secrets in the skill memory folder and review local logs or reports before sharing, syncing, or backing them up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bw520333/bw-openclaw-boost) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local status reports, memory notes, and configuration files under the skill directory.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
