## Description: <br>
Continuous session event recording for inter-session memory survival. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivaavimusic](https://clawhub.ai/user/ivaavimusic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep concise local session summaries so recent context can survive crashes, restarts, or session boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session summaries may contain privacy-sensitive context. <br>
Mitigation: Use the shortest retention period that works and avoid logging secrets, tokens, private keys, regulated data, or confidential details. <br>
Risk: Cleanup settings can write logs or delete session files in unexpected locations if paths are misconfigured. <br>
Mitigation: Review AGENTS.md, HEARTBEAT.md, the sessions directory, cleanup.sh, and any cron entry before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivaavimusic/ccp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown session notes with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes concise local session summaries and supports configurable log retention.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
