## Description:

Deprecated ClawHub skill that preserves historical GEO social publishing steps and directs users to the SaaS Word/ZIP plus local publishing workflow instead of installing or invoking the skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can read this archived skill to understand the deprecated GEO social publishing workflow and migrate to the replacement SaaS Word/ZIP plus local publishing process. It should not be installed or invoked as an active publishing skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated skill still contains live install, credential, curl, and publishing commands.

Mitigation: Treat the artifact as archival documentation only and do not install or invoke the retained commands unless the package and intended external actions have been independently verified.

Risk: The retained workflow can use saved credentials and publish or report content to external services.

Mitigation: Use the replacement SaaS Word/ZIP plus local publishing workflow described at the top of the artifact, and review any credential or publishing action before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/skills/geo-social-publish)
- [GEO SaaS base URL](https://ai.gaobobo.cn)
- [Archived social-auto-upload package URL](https://ai.gaobobo.cn/downloads/social-auto-upload.zip)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deprecated archival guidance; retained commands can install local tooling, use credentials, and publish or report content externally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
