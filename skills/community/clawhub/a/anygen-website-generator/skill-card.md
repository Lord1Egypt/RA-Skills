## Description:

Generates websites and landing pages through the AnyGen CLI and supporting website-generation workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create websites or landing pages such as product pages, portfolio sites, event pages, pricing pages, blogs, signup pages, app download pages, and campaign pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website-generation prompts or related content may be sent to AnyGen.

Mitigation: Avoid using the skill with private customer data, unpublished product details, secrets, or regulated content unless that transfer has been reviewed and approved.

Risk: The skill relies on external tools or workflow components that may not be pinned.

Mitigation: Use a pinned or reviewed AnyGen CLI and workflow version before using the skill in sensitive or production contexts.

Risk: The skill can install an additional workflow skill when it is unavailable.

Mitigation: Require explicit approval before installing additional skills or dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/logictortoise/skills/anygen-website-generator)
- [Publisher profile](https://clawhub.ai/user/logictortoise)
- [AnyGen website](https://www.anygen.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with CLI commands and workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the anygen binary and ANYGEN_API_KEY; generated website assets are produced through the AnyGen workflow.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
