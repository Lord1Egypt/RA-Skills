## Description:

EMP is an OpenClaw skill for empathetic, role-based task routing through OpenRouter-backed specialist roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzj0402](https://clawhub.ai/user/zzj0402)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use EMP to route prompts to specialized roles such as engineering, security, operations, customer success, and NVC coaching, then receive responses structured as observation, feeling, need, and request fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can replace the workspace-level SOUL.md and persistently change OpenClaw behavior beyond the skill directory.

Mitigation: Back up any existing ~/.openclaw/workspace/SOUL.md, review the EMP SOUL.md identity rules, and install the shell deployment step only when workspace-wide behavior changes are intended.

Risk: Prompt content is sent to OpenRouter-backed external models when the skill executes.

Mitigation: Avoid using EMP with confidential prompts unless external OpenRouter processing is acceptable for the deployment.

## Reference(s):

- [ClawHub EMP skill page](https://clawhub.ai/zzj0402/skills/emp)
- [OpenRouter](https://openrouter.ai/)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Structured NVC response fields with role and model metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY for model calls; role selection is keyword based unless a role is provided explicitly.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter and package.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
