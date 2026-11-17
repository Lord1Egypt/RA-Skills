## Description:

Guides Feishu custom-app administrators through diagnosing and fixing bots that cannot join external groups or appear in group bot search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators of Feishu custom-app bots use this skill to diagnose group membership and discoverability issues, enable external-group access through the app release workflow, or choose an internal-group alternative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials or tenant access tokens could be exposed during API diagnostics.

Mitigation: Keep app_secret and tenant_access_token private and confirm requests go to open.feishu.cn.

Risk: A diagnostic message could reach an unintended group.

Mitigation: Use a dedicated test chat when checking message permissions.

Risk: Enabling external-group use changes the app's availability.

Mitigation: Review the external-sharing setting and obtain administrator approval before relying on the published change.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jes614753-sketch/skills/feishu-external-group-fix)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and step-by-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an API diagnostic sequence, external-sharing release steps, and an internal-group alternative.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
