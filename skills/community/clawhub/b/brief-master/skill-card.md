## Description: <br>
Write precise execution briefs for agents, cron jobs, reviewers, researchers, and delegated coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, reviewers, researchers, and operators use Brief Master to turn vague requests into concise execution briefs with scope, constraints, non-goals, acceptance criteria, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs can direct autonomous agents to run commands, change code, use external services, schedule jobs, or publish content. <br>
Mitigation: Review generated briefs before execution, especially commands, credentials, scheduled jobs, public posting, elevated access, and changes to code or system state. <br>
Risk: A brief may be under-specified if critical inputs, constraints, paths, or acceptance criteria are missing. <br>
Mitigation: Use the skill's clarification step and 95 percent confidence gate so missing blockers are resolved before work begins. <br>
Risk: Invented credentials, secret names, hostnames, approvals, repository permissions, or schedules could mislead a downstream agent. <br>
Mitigation: Do not invent access details; mark elevated access, remote execution, persistent automation, and public posting as requiring explicit approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/brief-master) <br>
- [9 Dimensions of Intent](references/9-dimensions.md) <br>
- [Brief Formats](references/brief-formats.md) <br>
- [Messy Request To Clean Brief](examples/messy-to-clean-brief.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown execution brief with acceptance criteria, constraints, non-goals, and verification commands when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asks at most three clarifying questions when critical information is missing and removes wording that does not change the task.] <br>

## Skill Version(s): <br>
0.2.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
