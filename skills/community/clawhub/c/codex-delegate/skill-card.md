## Description:

Decide when to delegate a task to Codex and when to keep it in the main agent thread.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, and agent operators use this skill to decide whether code-heavy, repository-heavy, or environment-sensitive work should be delegated to Codex while the main agent keeps final judgment and user-facing ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegation guidance could be applied too broadly, causing the main agent to hand off final judgment or user-facing ownership.

Mitigation: Keep final risk trade-offs, environment acceptance, and completion decisions with the main agent as described by the skill.

Risk: A routing recommendation may be treated as proof that a technical result works in the user's actual environment.

Mitigation: Validate runtime behavior in the relevant shell, gateway, cron, LaunchAgent, or other target environment before calling work complete.

## Reference(s):

- [Codex Delegate skill page](https://clawhub.ai/g-hanasq/skills/codex-delegate)
- [Codex Delegate Routing Notes](references/routing.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise text or Markdown routing recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports conclusion, delegation decision, Codex scope, main-agent ownership, and validation level.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
