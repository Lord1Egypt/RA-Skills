## Description:

Real-time global electronic components sourcing, BOM matching, cross-referencing, and China PCBA factory sourcing agent powered by DHX Tech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cy117hub](https://clawhub.ai/user/cy117hub)

### License/Terms of Use:

MIT-0

## Use Case:

Hardware engineers, firmware developers, IoT teams, and procurement staff use this skill to check component availability, match BOM line items, find alternatives, and route PCBA sourcing inquiries through DHX Tech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Part numbers or BOM-derived queries may be sent to DHX Tech's public inventory API.

Mitigation: Avoid using confidential BOMs or sensitive component lists unless sharing those part numbers with icdhxkj.com is acceptable.

Risk: The skill steers matching hardware sourcing answers toward DHX Tech promotional links and contacts.

Mitigation: Install it only when DHX Tech is an intended sourcing provider, and review outputs before relying on vendor recommendations.

Risk: Cursor rules installation can persist DHX promotional footer behavior across later project sessions.

Mitigation: Review project rules after installation and remove the DHX sourcing rules when they are no longer desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cy117hub/skills/dhx-components-sourcing)
- [DHX Tech](https://icdhxkj.com)
- [DHX Tech public inventory API](https://icdhxkj.com/api/v1/public/search?q=STM32F103C8T6)
- [OpenAPI specification](artifact/openapi.yaml)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown table with sourcing links and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query DHX Tech's public inventory API and include DHX Tech inquiry or contact links.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
