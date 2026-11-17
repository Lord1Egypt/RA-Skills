## Description:

Runs a structured adversarial multi-agent review loop for significant documents, using reviewer personas to produce redlines, positions, and revised markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scott3j](https://clawhub.ai/user/scott3j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document authors use this skill to run adversarial reviews on substantial plans, designs, workflows, schemas, security designs, APIs, or positioning documents before acting on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe shell handling in the artifact scripts.

Mitigation: Manually review scripts before installation, remove eval from scripts/cp-output.sh, and validate session names, slugs, and destination paths before execution.

Risk: Reviewed documents may be stored locally and sent in full to spawned reviewer models.

Mitigation: Use only with documents approved for that storage and model-processing posture, and avoid confidential or regulated content unless the deployment has explicit approval.

Risk: The security guidance flags broad self-triggering and external reviewer spawning.

Mitigation: Require explicit user confirmation before spawning external reviewer sessions or running the review loop.

Risk: Reviewed document content can carry prompt-injection attempts into reviewer prompts.

Mitigation: Add clear prompt-injection boundaries around reviewed document content and treat reviewed text as untrusted input.

## Reference(s):

- [Redline Format Specification](references/redline-format.md)
- [Review Type Bundles](references/review-types.md)
- [Reviewer Personas](references/reviewer-personas.md)
- [ClawHub Skill Page](https://clawhub.ai/scott3j/skills/adversarial-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown with structured redline blocks, position notes, shell commands, and revised document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local review-session files under ~/.openclaw/workspace/reviews, including copied input documents, reviewer redlines, synthesized redlines, positions, and revised markdown output.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
