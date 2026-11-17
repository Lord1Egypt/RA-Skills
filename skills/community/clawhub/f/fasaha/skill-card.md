## Description:

Fasaha reviews and revises AI-generated or AI-translated Arabic so it reads as fluent native Modern Standard Arabic, checking Latin-script leakage, calques, terminology, grammar, punctuation, hamza spelling, and dialectal leakage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelpro](https://clawhub.ai/user/adelpro)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, translators, and content reviewers use Fasaha when translating into Arabic, drafting Arabic prose, or proofreading AI-generated Arabic for MSA fluency and correctness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to save user-derived register preferences, terminology, and failure patterns into shared skill reference files.

Mitigation: Use the skill directory read-only, or store such updates in a per-user or per-project location with explicit confirmation before saving.

## Reference(s):

- [QALB Guidelines v0.90](http://nlp.qatar.cmu.edu/qalb/QALB-guidelines_0.90.pdf)
- [Source bibliography](references/sources.md)
- [Fasaha checklist](references/checklist.md)
- [Dialect classification reference](references/dialect-classification.md)
- [Arabic spelling and punctuation rules](references/qalb-spelling-rules.md)
- [Machine translation examples](references/mt-examples.md)
- [Arabic terminology glossary](references/terminology.md)
- [Arabic voice and register profile](references/voice-profile.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Revised Arabic prose with concise Markdown review notes when a quality pass is reported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to register, terminology, or failure-log reference files when user preferences or recurring errors are identified.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
