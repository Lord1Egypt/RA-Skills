## Description:

Helps families coordinate elder-care tasks, medication check-ins, visit preparation, caregiver handoffs, and emergency information using locally stored records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Family caregivers and helpers use this skill to assign care responsibilities, track observations and refills, and prepare printable day sheets, visit briefs, handoffs, and emergency cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive elder-care details are stored in an unencrypted local file.

Mitigation: Keep the state file in a private directory and avoid public or loosely shared sync folders.

Risk: Outdated or incorrect family-maintained information could appear in visit briefs or emergency cards.

Mitigation: Check records with caregivers and clinicians, verify generated documents before use, and regenerate cards after medication changes.

## Reference(s):

- [Family Care Coordination Playbook](references/family-care-playbook.md)
- [ClawHub skill listing](https://clawhub.ai/voronindenis5/skills/elder-care-coordinator)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text, including printable care summaries and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses family-maintained local records; not clinical advice or an emergency service.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
