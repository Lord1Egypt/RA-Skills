## Description:

Generates and compares Spanish short-video hook variants from a script or viral reference, optionally producing test clips with Higgsfield and ranking them with Virality Predictor before returning a production brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media teams, and content strategists use this skill to generate 2-4 differentiated first-second hook concepts for Spanish-language short videos, test optional AI clips with Higgsfield, and choose a winning production brief before recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generated media, and user-provided reference images may be sent to Higgsfield or Apify when those integrations are used.

Mitigation: Confirm the user is comfortable sharing that material with the connected services before running integrations.

Risk: AI media generation and predictor runs can consume external service credits.

Mitigation: Disclose expected credit cost and wait for explicit approval before generation.

Risk: Using a person's face, private material, or reference images without consent can create privacy and likeness concerns.

Mitigation: Use real-person imagery only with consent and avoid private material unless the user has permission to use it.

Risk: The workflow requires neutral Spanish and may not match audiences expecting a different dialect.

Mitigation: Adjust the language requirement when the target audience expects a different Spanish voice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/generador-ganchos-formula100k)
- [criterios.md](artifact/criterios.md)
- [moldes-gancho.md](artifact/moldes-gancho.md)
- [output-template.md](artifact/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown report in Spanish with optional PNG, MP4, JSON job mapping, and Higgsfield dashboard links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 2-4 hook variants, a ranked LAB report, a winning production brief, and optional generated media artifacts when Higgsfield integrations are connected.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
