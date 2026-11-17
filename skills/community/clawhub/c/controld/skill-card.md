## Description:

Manage Control D DNS filtering service via API for DNS profiles, devices, custom blocking rules, service filtering, analytics settings, and network diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austingarrod](https://clawhub.ai/user/austingarrod)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and DNS administrators use this skill to inspect and manage Control D DNS filtering accounts, including profiles, devices, filters, service rules, analytics, and enterprise deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Control D account changes, including deletes, organization updates, default-rule changes, provisioning changes, and mass deployment actions.

Mitigation: Use least-privilege or read-only tokens where possible and require manual confirmation before destructive, billable, organization-wide, or mass deployment operations.

Risk: The skill depends on a Control D API token that may grant write access to DNS profiles, devices, analytics, and organization resources.

Mitigation: Store the token outside prompts and files, restrict it by IP where possible, and rotate it if exposed.

Risk: The documented RMM installer one-liners can execute remote endpoint deployment commands at scale.

Mitigation: Independently verify the installer source, signature or checksum, and test deployment in a controlled environment before use across endpoints.

## Reference(s):

- [Control D](https://controld.com)
- [Control D Dashboard](https://controld.com/dashboard)
- [Control D API Base URL](https://api.controld.com)
- [ClawHub Skill Page](https://clawhub.ai/austingarrod/skills/controld)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON API examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CONTROLD_API_TOKEN plus curl and jq for the bundled helper script.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
