## Description:

A first-principles strategic decision wargame that guides agents through a three-layer, nine-question framework for evaluating business directions, strategic moves, product lines, and transformations with premortem analysis, timing checks, mental models, exit conditions, and reviewable decision records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clongin](https://clawhub.ai/user/clongin)

### License/Terms of Use:

MIT-0

## Use Case:

Business leaders, founders, strategy teams, and their agents use this skill to pressure-test candidate business directions or strategic actions before committing resources. It produces a structured decision card with assumptions, risks, milestones, exit conditions, and review timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for confidential company strategy, team, financial, or market context.

Mitigation: Use only information approved for the agent session, and redact sensitive details when possible.

Risk: Broad trigger phrases could activate the full decision framework during ordinary planning conversations.

Mitigation: Invoke the skill explicitly and confirm that a strategic wargame is intended before applying the framework.

Risk: Strategic recommendations may be misleading if the user provides incomplete assumptions or unverified evidence.

Mitigation: Treat outputs as decision-support artifacts and require review by accountable human decision owners before committing resources.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/clongin/skills/first-principles-wargame)
- [Mental model library, red flags, and cases](references/framework.md)
- [Premortem protocol](references/premortem-protocol.md)
- [Timing framework](references/timing-framework.md)
- [Decision output template](assets/wargame-output-template.md)
- [Mainline discovery worksheet](assets/mainline-discovery-worksheet.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown decision analysis with optional command-line scoring output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include decision cards, tables, premortem findings, milestones, exit criteria, and a next review date.]

## Skill Version(s):

2.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
