## Description:

Turn health notes, transcripts, or check-ins into non-diagnostic 8D pattern reviews with confidence levels and safe next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divinity-science](https://clawhub.ai/user/divinity-science)

### License/Terms of Use:

MIT-0

## Use Case:

External users and wellness-focused agents use this skill to turn health notes, transcripts, check-ins, or journal entries into concise, non-diagnostic 8D wellness pattern reviews. It maps supported signals to wellness dimensions, states confidence, and offers one low-risk next step while redirecting diagnosis, treatment, medication, and urgent symptoms to professional care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles health-related notes and could be misused as diagnosis, treatment planning, medication guidance, or emergency triage.

Mitigation: Keep outputs non-diagnostic, stay within user-provided evidence, provide only low-risk next steps, and redirect urgent or serious symptoms to clinicians or emergency services.

Risk: Sparse wellness notes can lead to overconfident pattern claims.

Mitigation: State confidence explicitly, narrow conclusions when evidence is thin, avoid fabricated scores, and ask for one clarifying detail when needed.

## Reference(s):

- [8D Dimensions Guide](artifact/8d-dimensions-guide.md)
- [Project homepage](https://github.com/divinity-science/8d-pattern-awareness)
- [ClawHub skill page](https://clawhub.ai/divinity-science/skills/8d-wellness-awareness)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with labeled sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-diagnostic wellness pattern review with confidence, safe next step, and watch-outs.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
