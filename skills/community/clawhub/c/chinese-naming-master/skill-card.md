## Description:

天衡命名宗师 helps agents collect required personal naming details and produce structured Chinese personal-name candidates grounded in traditional naming frameworks, classical references, phonology, and practical name-quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longge0516](https://clawhub.ai/user/longge0516)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for Chinese personal naming, adult name changes, and Chinese name analysis. It guides the conversation through required birth and family-name context, then returns ranked name candidates with cultural, phonological, zodiac, Five Elements, and usability analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for personal naming details including birth date, birth time, gender, surname, generational-name rules, and optional parent names.

Mitigation: Collect only the naming details the user chooses to provide, avoid unnecessary family details, and make clear that sharing this context is optional.

Risk: Traditional naming analysis could be mistaken for deterministic life or fate guidance.

Mitigation: Present Five Elements, zodiac, and name-structure analysis as cultural interpretation and do not claim that a name determines life outcomes.

Risk: Incomplete birth-time information lowers the precision of the requested Five Elements analysis.

Mitigation: Ask for birth time before analysis and disclose reduced precision when the user cannot provide it.

## Reference(s):

- [八步命名法详细框架](references/naming-framework.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured Chinese-name candidate analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five ranked candidate personal names with required sections for generational-name constraints, source text, meaning, Five Elements, zodiac fit, name-structure checks, phonology, homophone risk, overall meaning, and scoring.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
