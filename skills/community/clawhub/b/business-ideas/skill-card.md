## Description:

Generate unlimited business ideas with validation frameworks, market filters, and viability scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to generate, filter, score, and validate startup, side-project, and business ideas, with optional local memory for prior ideas and preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated business ideas, favorites, rejection notes, and preferences may be stored in ~/business-ideas/ and reused by later local agent sessions.

Mitigation: Avoid saving confidential business plans or sensitive preferences there unless local reuse is acceptable; ask the agent before saving when tighter control is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/business-ideas)
- [Skill Homepage](https://clawic.com/skills/business-ideas)
- [Idea Generation Frameworks](frameworks.md)
- [Memory Setup - Business Idea Generator](memory-template.md)
- [Idea Validation Methods](validation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with ranked tables, scorecards, checklists, and occasional shell commands for local memory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist generated ideas, favorites, rejection notes, and preferences in ~/business-ideas/ when the user allows local memory updates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
