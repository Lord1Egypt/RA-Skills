## Description:

Use when you want to acquire, improve, or master a manual, trade, craft, or embodied skill through personalized deliberate practice regimens, targeted drills, progress logs, feedback loops, and adjustment based on user reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent plan and track deliberate practice for hands-on skills while they perform the physical work. It is intended for learning or improving manual, trade, craft, instrument, tool-handling, gardening, and other embodied skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses npx without a pinned trusted installer version.

Mitigation: Use a pinned or otherwise trusted ClawHub installer version and run installation from a normal least-privileged account.

Risk: The skill may create or update practice logs and planning files for the manual skill being coached.

Mitigation: Review generated or modified files and keep practice logs in an expected workspace.

Risk: Manual-skill practice can involve physical injury or legal certification requirements.

Mitigation: Use proper form, low-stakes materials, professional oversight for high-risk activities, and qualified instructors or certification paths where required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/deliberate-practice-for-manual-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, files, shell commands]

**Output Format:** [Markdown guidance, practice plans, checklists, resource lists, and practice-log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses filesystem access to create or update practice logs and planning files when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
