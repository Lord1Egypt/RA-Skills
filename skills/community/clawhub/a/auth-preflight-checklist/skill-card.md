## Description:

Preflight checklist for auth-dependent work: verify the active credential lane, runtime environment, scopes, and smallest safe live probe before writing, deploying, or debugging provider integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before auth-dependent documentation, troubleshooting, scheduled jobs, deploys, API integrations, or provider debugging to confirm the active credential lane, runtime environment, scopes, and smallest safe live probe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live auth probe may touch real provider resources or reveal sensitive credential state if it is broader than needed.

Mitigation: Review each proposed probe before execution, keep probes read-only or minimally safe, and do not print or share secret values.

Risk: Auth-dependent work may continue after a missing credential, 401, 403, or insufficient scope result.

Mitigation: Stop writes and deploys after auth failure unless the task explicitly asks for forensic collection, and record the missing auth lane, expected secret reference, runtime, probe result, and next owner or action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/auth-preflight-checklist)
- [ClawHub publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown checklist with concise guidance and proposed read-only probe commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill advises checking credential presence without printing secret values and recording blockers when auth cannot be verified.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
