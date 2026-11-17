## Description:

Galdr helps agents analyze local audio and create time-ordered listening prompts grounded in audio-derived structural cues, not measured listener responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sellemain](https://clawhub.ai/user/sellemain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can analyze a supplied local audio file and create a grounded, time-ordered listening experience or evidence prompt using Galdr's audio-derived structure cues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separately installed CLI may not match the skill's targeted version or trusted source.

Mitigation: Verify the CLI's source and version before use.

Risk: Analysis files remain on disk after processing.

Mitigation: Review and manage generated analysis files according to the sensitivity of the audio and context.

Risk: Generated prompts and supplied context may be sent to an external model.

Mitigation: Review both and explicitly authorize transmission before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sellemain/skills/galdr)
- [Metrics reference](artifact/references/metrics.md)
- [Galdr on PyPI](https://pypi.org/project/galdr/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prompts or listening-experience prose; raw analysis may be structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-ordered audio-derived cues; interpretation prompts are not measured listener responses.]

## Skill Version(s):

0.8.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
