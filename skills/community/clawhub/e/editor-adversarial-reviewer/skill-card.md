## Description:

Provides a Chinese-language adversarial script review workflow that scores scripts across hook, motivation, cliche, emotional manipulation, and irreplaceability dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal)

### License/Terms of Use:

MIT-0

## Use Case:

Screenwriters, editors, and story development agents use this skill to run a Chinese-language adversarial review after script self-checks, identify story-quality failures, and decide whether rewrite is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Script content is sent into an isolated subagent for critique.

Mitigation: Use it only for scripts approved for agent review and keep the isolated-review workflow described by the artifact.

Risk: The workflow is intentionally strict and may recommend rejection or mandatory rewrites.

Mitigation: Treat verdicts as editorial review input and have a responsible editor confirm rewrite decisions.

Risk: The checklist is designed for Chinese-language adversarial script review.

Mitigation: Use it for that intended review posture, or adapt the criteria before applying it to other languages or review styles.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huangliujiao-tal/skills/editor-adversarial-reviewer)
- [Publisher Profile](https://clawhub.ai/user/huangliujiao-tal)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with scored review notes, verdict, mandatory rewrites, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language critique focused on story quality; no file edits are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
