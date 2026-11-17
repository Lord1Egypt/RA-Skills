## Description:

Helps people facing AI-driven white-collar job displacement assess transferable skills, compare realistic career paths, and plan a financially viable transition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

People whose white-collar roles have been or may be displaced by AI use this skill to audit their transferable skills, evaluate practical career options, and build a transition plan that accounts for training time, costs, income floor, local demand, and financial runway.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill may store sensitive career, savings, expense, and financial-runway details when persistence is enabled.

Mitigation: Use persistence only in a trusted environment and keep stored state limited to the minimum needed for the transition plan.

Risk: Calendar automation can create recurring reminders based on personal career-transition status.

Mitigation: Enable calendar access only after reviewing the proposed reminders and confirming the schedule is useful.

Risk: Filesystem access is requested broadly by the skill metadata.

Mitigation: Restrict filesystem access to a dedicated skill or notes directory where supported.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/career-reinvention)
- [Bureau of Labor Statistics Occupational Outlook Handbook](https://www.bls.gov/ooh/)
- [O*NET OnLine](https://www.onetonline.org/)
- [CareerOneStop](https://www.careeronestop.org/)
- [U.S. Department of Labor WIOA Programs](https://www.dol.gov/agencies/eta/wioa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance with structured markdown checklists, evaluation prompts, transition plans, optional install command, and optional YAML state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use browser, calendar, and filesystem tools when enabled; includes optional recurring progress and financial-runway check-ins.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
