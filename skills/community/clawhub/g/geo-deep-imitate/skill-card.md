## Description:

Geo Deep Imitate uses web_fetch to gather reference sources, generate deep imitation content through the GEO service, export a ZIP, and report completion to the GEO workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus)

### License/Terms of Use:

MIT-0

## Use Case:

External GEO workflow users and developers use this skill to fetch reference sources, generate deep imitation content through the GEO SaaS API, export the resulting ZIP, and report the branch as complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists a GEO API key in plaintext on the local filesystem.

Mitigation: Use a platform secret manager when available, restrict ~/.qclaw/geo-api-key to owner-only permissions, and rotate the key if it may have been exposed.

Risk: The skill contacts the GEO SaaS service with an API key and may submit source material and task metadata there.

Mitigation: Install and run it only when that data transfer is intended, authorized, and acceptable for the workflow.

Risk: The security summary flags undeclared shell and API operations.

Mitigation: Review the local file writes, export path, and GEO API calls before installation and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/skills/geo-deep-imitate)
- [GEO SaaS service](https://ai.gaobobo.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can store GEO exports locally as a fangxie.zip file after the remote workflow completes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
