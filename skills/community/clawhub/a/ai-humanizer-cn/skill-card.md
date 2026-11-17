## Description:

Optimizes Chinese AI-generated text into a more natural human writing style while preserving a professional tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengong101](https://clawhub.ai/user/pengong101)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to rewrite Chinese AI-generated text for a more natural tone across professional, academic, business, blog, and casual styles. Review transformed text before using it in public, regulated, or high-stakes settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports inconsistent documentation: the package appears to perform local text rewriting, while documentation asks for AI provider API keys and claims remote-model features.

Mitigation: Do not provide AI provider API keys or sensitive documents until the release reconciles local-only versus remote-provider behavior and removes unimplemented claims.

Risk: Remote-model, batch, and bulk-processing behavior may not match the inspected code.

Mitigation: Validate the installed code path on non-sensitive sample content before relying on those features in production workflows.

Risk: Dependencies are not fully pinned or justified in the release evidence.

Mitigation: Pin or justify dependencies before deployment, and review dependency changes during release intake.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengong101/skills/ai-humanizer-cn)
- [Publisher profile](https://clawhub.ai/user/pengong101)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Plain text, Markdown, or code-oriented rewrite suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed for tone, factual accuracy, and privacy before use with sensitive documents.]

## Skill Version(s):

5.0.0 (source: server release metadata and SKILL.md frontmatter, updated 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
