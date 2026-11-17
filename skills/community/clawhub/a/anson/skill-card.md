## Description:

Bootstrap and personalize an AI assistant with a rich, bespoke identity, user profile, and working style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmundworks](https://clawhub.ai/user/edmundworks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Anson to bootstrap a personalized assistant by creating durable identity, user, relationship, and agent-instruction documents. It also scaffolds maker skills that can maintain those documents over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create long-lived profile, identity, and relationship files that store inferred user preferences or personal context.

Mitigation: Review generated personalization files before allowing writes and remove any content the user does not want preserved.

Risk: The skill can modify AGENTS.md or CLAUDE.md, which may affect how future agents behave in the workspace.

Mitigation: Inspect instruction-file diffs before accepting them and keep only lifecycle rules that match the user's intended assistant behavior.

Risk: The skill can create new maker skills that continue updating personalization state after bootstrap.

Mitigation: Scan and review generated skills before deployment, and install only when persistent personalization is acceptable.

## Reference(s):

- [Bootstrap process](references/bootstrap-process.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic skills repository](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, conversational guidance, scaffolded skill files, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write ANSON_META.md, IDENTITY.md, USER.md, SOUL.md, maker skills, and AGENTS.md or CLAUDE.md in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
