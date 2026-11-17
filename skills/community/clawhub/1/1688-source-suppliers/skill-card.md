## Description:

Finds 1688 suppliers and factories by querying the 1688 platform with user-provided supplier names, regions, industries, or keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and sourcing users use this skill to look up supplier and factory records on 1688, then return complete supplier summaries for the requested keyword without fabricating missing supplier data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential setup can expose or misstore the 1688 access key.

Mitigation: Provide the AK through a protected secret manager or controlled environment injection, avoid pasting it into ordinary chat or shell history, and rotate it if exposure is suspected.

Risk: Gateway-related environment variables can redirect where authenticated requests or configuration updates are sent.

Mitigation: Verify gateway URLs and tokens in the runtime environment before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-source-suppliers)
- [Publisher profile](https://clawhub.ai/user/1688aiinfra)
- [1688 supplier search](https://s.1688.com/company/company_search.htm)
- [references/capabilities/ali_1688_source_suppliers.md](artifact/references/capabilities/ali_1688_source_suppliers.md)
- [references/capabilities/configure.md](artifact/references/capabilities/configure.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses with user-facing Markdown supplier summaries and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and an ALI_1688_AK credential for authenticated supplier queries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
