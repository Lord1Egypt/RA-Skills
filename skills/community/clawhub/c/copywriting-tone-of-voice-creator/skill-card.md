## Description:

Builds or adapts a brand tone-of-voice guide in markdown, including voice attributes, tone modulation, lexicon, mechanics, inclusive-language guidance, and channel rules for downstream content agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, content, and developer teams use this skill to create a machine-readable TONE.md brand voice guide or adapt an existing guide to a new channel. The guide supports downstream writing agents and human writers who need consistent voice, tone, lexicon, mechanics, and channel-specific rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tone-of-voice guidance may be misaligned with the user's locale, audience, or regulatory context.

Mitigation: Review the generated guide against the intended market, audience, and applicable regulatory constraints before using it in production content workflows.

Risk: The skill can read supplied brand context and write or modify TONE.md-style markdown files.

Mitigation: Provide only appropriate brand materials and review file changes before downstream writing agents consume the guide.

Risk: For uncovered or regulated categories, the skill may use web research to shape category-specific tone guidance.

Mitigation: Verify research-derived claims and cited sources before relying on the resulting brand voice guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/copywriting-tone-of-voice-creator)
- [Project homepage](https://github.com/samber/cc-skills)
- [TONE template](assets/TONE-template.md)
- [Discovery questionnaire](references/discovery-questionnaire.md)
- [Category adaptations](references/category-adaptations.md)
- [Channel adaptations](references/channel-adaptations.md)
- [Voice attributes](references/voice-attributes.md)
- [Lexicon mechanics](references/lexicon-mechanics.md)
- [Reference brands](references/reference-brands.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files, primarily TONE.md or channel-specific TONE-<channel>.md guides]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-provided brand context, ask structured discovery questions, use web research for uncovered or regulated categories, and write or modify markdown guide files.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
