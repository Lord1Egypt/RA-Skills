## Description: <br>
Commitment Engine helps an agent record time-bound commitments in a persistent ledger, track status changes, and prepare or escalate tasks through heartbeat and cron checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dottythehomeless](https://clawhub.ai/user/dottythehomeless) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users can use this skill to turn explicit time-bound requests and recurring obligations into trackable commitments. It is intended for agents that need reminders, status transitions, and follow-up behavior without relying on short-term conversational memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user commitments and scheduled follow-up actions, which may retain sensitive tasks across sessions. <br>
Mitigation: Use it only when persistent commitment tracking is desired; review, change, cancel, and delete ledger entries and avoid sensitive commitments unless persistence is acceptable. <br>
Risk: The security review notes future cron-triggered actions without clear approval or cleanup controls. <br>
Mitigation: Confirm cron jobs before enabling them and periodically audit active commitments and scheduled jobs for obsolete or unintended actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dottythehomeless/commitment-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with ledger tables, state-machine guidance, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a commitments.md ledger and propose OpenClaw cron jobs for recurring commitments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
