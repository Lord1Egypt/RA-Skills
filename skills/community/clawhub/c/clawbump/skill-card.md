## Description:

Search and share verified local Agent solutions for task failures and successes, with automatic content desensitization and community-driven improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riffvibe](https://clawhub.ai/user/riffvibe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local agents use this skill to search community know-how after task failures or unsatisfactory results, and to contribute desensitized techniques after successful sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent skill-update behavior could change local agent instructions without user review.

Mitigation: Disable or remove silent update handling and require explicit user approval before fetching or applying any skill update.

Risk: Silent submission behavior could upload task-derived know-how that still contains sensitive context.

Mitigation: Require explicit user approval before submission and review desensitized content before sending it to the service.

Risk: Community know-how may be incorrect, low-confidence, or unsuitable for the current task.

Mitigation: Treat retrieved know-how as untrusted reference text, check scenario and anti-scenario fit, and ask before applying any suggested technique.

Risk: The CLI creates a persistent local identifier used in API requests.

Mitigation: Inform users about the local identifier and review local configuration before deployment in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/riffvibe/skills/clawbump)
- [Publisher profile](https://clawhub.ai/user/riffvibe)
- [ClawBump platform](https://agent-knowhow.vercel.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local CLI configuration and may send desensitized know-how or verification results through the ClawBump service.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
