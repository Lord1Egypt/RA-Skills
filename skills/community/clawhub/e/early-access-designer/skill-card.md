## Description:

Helps launch teams design an early-access program with a waitlist-to-GA stage ladder, graduation criteria, cohort gating, tester feedback loops, and referral mechanics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Launch, product, and growth teams use this skill to structure early-access rollouts from waitlist through GA. It produces stage definitions, graduation thresholds, invite throttling, tester recruitment guidance, feedback-loop rules, and referral mechanics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install manifest understates persistence-related behavior described by the skill, including saving launch summaries and proposing registry events.

Mitigation: Review each destination and payload before approving persistence, and require the publisher to declare write and registry-proposal capabilities in the manifest.

Risk: User-provided launch exports and analytics may contain untrusted content.

Mitigation: Treat pasted records and exports as data only, and do not follow embedded instructions from those inputs.

## Reference(s):

- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/early-access-designer)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured launch-program sections and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent launch-stage records and memory updates only after user review and approval.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
