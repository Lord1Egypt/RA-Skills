## Description: <br>
Configures OpenClaw cron jobs and memory rules to generate daily, weekly, monthly, quarterly, and yearly experience summaries and retrieve past experience on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17oko](https://clawhub.ai/user/17oko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to set up recurring summaries of conversation history and maintain longer-term memory files for later retrieval. It is intended for users who explicitly want automated local memory creation from their workspace activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deleted or reset conversations may be preserved in long-lived summaries. <br>
Mitigation: Exclude deleted/reset session files or add retention limits before enabling the scheduled summaries. <br>
Risk: Generated memory files may contain sensitive conversation content. <br>
Mitigation: Review generated memory files regularly and narrow retrieval to explicit user requests when privacy matters. <br>
Risk: Automated memory reuse may surface stale or inappropriate historical context. <br>
Mitigation: Use relevance thresholds, limit returned memories, and require user confirmation for sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/17oko/experience-summary-sys) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory files and AGENTS.md guidance when the user follows the setup steps.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
