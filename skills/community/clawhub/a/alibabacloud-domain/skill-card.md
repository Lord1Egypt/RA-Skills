## Description:

Manage Alibaba Cloud domains, DNS, ICP filing, and Wan Xiao Zhi websites through DomainCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and domain administrators use this skill to plan and carry out Alibaba Cloud domain registration, DNS changes, ICP filing, and website deployment with explicit approval for consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain purchases, DNS edits, publication, and deletion can incur charges or change live services.

Mitigation: Review the exact target, price or change preview, and impact; approve each consequential action only after its current preview.

Risk: Cloud credentials and domain or filing identity data may be sensitive.

Mitigation: Use scoped cloud credentials, keep secrets out of chat and saved output, and disclose only task-relevant fields.

Risk: The bundled manifest lacks the required skill name and may prevent operation.

Mitigation: Have the publisher correct the manifest before relying on the skill operationally.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-domain)
- [Domain operations](references/domain.md)
- [ICP filing](references/icp.md)
- [Website building](references/website.md)
- [Safety and confirmation](references/safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chat response with status footer and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Files only when explicitly requested; reports the result, evidence source, write effect, and next step.]

## Skill Version(s):

0.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
