## Description:

Guides users from a vague project idea through brand discovery, naming directions, and DomainKits-backed domain availability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abtdomain](https://clawhub.ai/user/abtdomain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn an early project description into domain naming directions, candidate domains, and verified acquisition paths. It supports consultative naming workflows that rely on DomainKits for availability and domain intelligence checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate names and domain-search queries are sent to DomainKits for availability and domain intelligence checks.

Mitigation: Install only if that data sharing is acceptable, and use the optional API key only when higher limits are needed.

Risk: Domain monitoring can track domains beyond the immediate naming session if enabled.

Mitigation: Enable monitoring only for domains the user intentionally wants watched.

Risk: Unverified domain suggestions could mislead users about availability.

Mitigation: Present a domain as available only after verification with DomainKits availability checks.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/abtdomain/skills/domain-generator)
- [DomainKits MCP](https://domainkits.com/mcp)
- [DomainKits pricing](https://domainkits.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with conversational prompts, domain result lists, and optional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available-domain claims must be backed by DomainKits availability checks before presentation.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
