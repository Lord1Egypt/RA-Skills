## Description: <br>
Automatically record and analyze user behavior patterns from conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chefroger](https://clawhub.ai/user/chefroger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers use this skill to track local conversation-derived patterns such as recurring topics, project focus, active hours, and skill usage. It can produce manual or scheduled summaries for personal behavior review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived behavior files may contain sensitive personal or project information. <br>
Mitigation: Review the OpenClaw workspace memory directory before use, restrict access to generated files, and delete behavior data or reports when the profile is no longer wanted. <br>
Risk: Cron or heartbeat automation can continue analyzing local memory over time. <br>
Mitigation: Enable scheduled tracking only with informed consent and disable cron or heartbeat automation when ongoing analysis is not desired. <br>
Risk: Keyword-based summaries can be incomplete or misleading if used as definitive behavioral conclusions. <br>
Mitigation: Treat reports as personal review aids and inspect the underlying local memory data before making decisions from the summaries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chefroger/behavior-tracker) <br>
- [Publisher Profile](https://clawhub.ai/user/chefroger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON behavior data, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local behavior pattern data, report output, and heartbeat state under the OpenClaw workspace memory directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
