## Description:

Transform a foreign identity into a Chinese cultural identity package with meaningful Chinese name options, classical poetry, seal-carving art prompts, ink-wash landscape prompts, and ancient-style portrait avatar prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoaipensieve](https://clawhub.ai/user/xiaoaipensieve)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to guide a personalized Chinese cultural naming and art workflow, including name selection, poem generation, cultural explanation, and image-generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles identity-related inputs such as names, preferences, poems, and generated art context with configured AI providers.

Mitigation: Review provider data-sharing expectations before installation, minimize retained personal context, and disclose external model use to users.

Risk: Broad triggers, session memory, and telemetry can make collection or retention behavior unclear to users.

Mitigation: Require explicit confirmation before full-package generation, keep identity data session-scoped, and disable or review telemetry where appropriate.

Risk: Dependencies are listed with broad version ranges.

Mitigation: Install in an isolated environment with pinned, reviewed dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoaipensieve/skills/cultural-naming-art)
- [Publisher profile](https://clawhub.ai/user/xiaoaipensieve)
- [Tencent SkillHub listing declared in artifact metadata](https://skilhub.cloud.tencent.com/skills/cultural-naming-art)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style conversational responses with structured name options, poems, explanations, and image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated-art prompt text and package-style summaries for seal, landscape, and portrait outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and manifests declare 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
