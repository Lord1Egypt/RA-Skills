## Description:

Helps families create and adjust weekly child development schedules, check time conflicts, and generate weekly reviews while minimizing child and household data collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

External caregivers and families use this skill to turn family constraints, child preferences, and development goals into practical weekly schedules, conflict checks, and review templates. It can optionally prepare Feishu or Notion persistence steps after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child and family scheduling information can be sensitive, and the security summary notes that the child profile template asks for more detail than the skill's privacy-minimization rules require.

Mitigation: Use aliases, age bands, and broad time constraints; avoid real names, schools, addresses, precise locations, medical details, and unnecessary household details.

Risk: Optional Feishu or Notion persistence could save family records longer or more broadly than intended.

Mitigation: Enable integrations only after reviewing the exact fields, records, retention period, and target workspace or database; use least-privilege connectors and confirm each read, write, push, overwrite, or deletion separately.

Risk: Generated family schedules or reward plans may be too ambitious or unsuitable for a child's current condition.

Mitigation: Treat outputs as editable planning drafts, preserve sleep, meals, movement, recovery, and free time, and seek qualified professional advice for persistent health, developmental, or behavioral concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/family-cultivation-coach)
- [Project homepage](https://github.com/yangchao228/family-baby-asistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration guidance]

**Output Format:** [Markdown schedules and weekly reviews with optional structured JSON schedule blocks and integration setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to session-only output; external Feishu or Notion reads, writes, pushes, deletion, and retention changes require explicit scope confirmation.]

## Skill Version(s):

1.6.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
