## Description:

Injury prevention through proper body mechanics for physical work, including safe lifting, carrying, standing, repetitive-motion prevention, warmups, and early warning signs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents use this skill to provide general injury-prevention guidance for people with physically demanding jobs, including lifting, carrying, standing, repetitive strain prevention, warmups, and escalation cues for pain or injury.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access and uses an unpinned npx installer.

Mitigation: Review the package-manager setup path before installation and restrict filesystem access for the skill.

Risk: Users may treat general body-mechanics guidance as medical care.

Mitigation: Use the skill for prevention guidance only, stop if symptoms worsen, and consult a licensed clinician for pain, numbness, injury history, pregnancy, balance issues, or other medical limitations.

## Reference(s):

- [NIOSH](https://www.cdc.gov/niosh/)
- [OSHA Ergonomics](https://www.osha.gov/ergonomics)
- [American Physical Therapy Association](https://www.apta.org)
- [Bureau of Labor Statistics Injuries, Illnesses, and Fatalities](https://www.bls.gov/iif/)
- [Anthropic Labor Market Impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured checklists and plain-language instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt workplace safety references, units, and standards to the user's region.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
