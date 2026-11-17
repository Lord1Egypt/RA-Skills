## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can preserve reusable lessons and improve future workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adityasagar2](https://clawhub.ai/user/adityasagar2)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to record corrections, failed commands, requested capabilities, and recurring practices into learning files. They can then review and promote vetted learnings into persistent agent instructions or new reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning notes may preserve sensitive conversation details or project context longer than intended.

Mitigation: Keep logs local where possible and redact secrets, credentials, private data, and unnecessary user context before saving entries.

Risk: Promoting learnings into persistent agent memory or instruction files can spread incorrect or overly broad guidance.

Mitigation: Require explicit human review before promotion and keep promoted guidance concise, scoped, and reversible.

Risk: Global hooks or cross-session sharing can increase exposure of captured context.

Mitigation: Enable hooks and cross-session sharing only where needed, prefer project-scoped configuration, and review hook output before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adityasagar2/skills/aditya)
- [OpenClaw integration](references/openclaw-integration.md)
- [Hook setup guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and learning-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning files and propose promotions to agent instruction files when the user enables those workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
