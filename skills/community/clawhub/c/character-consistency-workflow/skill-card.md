## Description:

A Chinese-language workflow that helps creators reduce character drift in AI-generated short videos by preparing reference assets, writing consistency tokens, and checking cross-shot appearance, costume, and expression continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beermanzz](https://clawhub.ai/user/beermanzz)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video teams, and prompt writers use this skill to keep the same character visually consistent across AI-generated shots. It provides asset preparation guidance, reusable character-token templates, prompt construction patterns, and quality checks for character drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can involve real performer or model reference photos and detailed appearance metadata.

Mitigation: Obtain consent, keep reference assets and meta.json private, and delete or minimize sensitive appearance details when they are no longer needed.

Risk: Character-locking prompts and reference images could be misused to imitate a real person without authorization.

Mitigation: Use only authorized likenesses and review generated outputs before release for consent, rights, and disclosure requirements.

## Reference(s):

- [Asset Preparation Guide](references/asset-preparation.md)
- [Consistency Tokens Guide](references/consistency-tokens.md)
- [ClawHub Skill Page](https://clawhub.ai/beermanzz/skills/character-consistency-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with prompt templates, checklists, tables, and example directory structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only output; no executable code or hidden automation is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
