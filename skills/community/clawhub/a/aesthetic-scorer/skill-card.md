## Description:

Scores and analyzes photo aesthetics with local image scoring models, then provides concise bilingual feedback and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

Photographers, content creators, and agents use this skill to score image aesthetics, compare photos, and generate composition, color, lighting, technical quality, and improvement feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup depends on third-party ML repositories and packages that may change over time.

Mitigation: Install in an isolated virtual environment or container and pin or verify repository commits and package versions before use.

Risk: The skill makes strong offline and privacy claims while initial setup may require external downloads.

Mitigation: Treat offline privacy claims as applying to local runtime image scoring after dependencies and model weights have been obtained and verified.

Risk: Running ML setup or scoring scripts with elevated privileges increases impact if dependencies are compromised.

Mitigation: Avoid administrator or root execution and restrict filesystem access to only the images and model files needed for scoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/aesthetic-scorer)
- [Improved Aesthetic Predictor](https://github.com/christophschuhmann/improved-aesthetic-predictor)
- [NIMA Neural Image Assessment](https://github.com/titu1994/neural-image-assessment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with numeric scores, rating labels, analysis sections, and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports brief, medium, detailed, and multi-photo comparison reports in Chinese or English.]

## Skill Version(s):

1.4.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
