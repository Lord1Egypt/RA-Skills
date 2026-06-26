## Description: <br>
Runs lightweight self-audits of OpenClaw behavior to find repeated failures, propose safe configuration or process improvements, and track changes after incidents, silent-bot periods, rate-limit spikes, or weekly maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw reliability, group recurring failures, identify likely root causes, propose reversible fixes, and record follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can restart OpenClaw services or make small configuration changes when used as written. <br>
Mitigation: Require approval for restarts, session cleanup, and configuration changes on production systems, and keep rollback notes for each applied change. <br>
Risk: Maintenance reports could expose sensitive operational details if logs or summaries include secrets. <br>
Mitigation: Do not expose secrets in reports, and review collected logs before sharing summaries outside the operating team. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/utromaya-code/agent-self-improver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with audit summaries, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed low-risk maintenance actions and rollback notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence, released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
