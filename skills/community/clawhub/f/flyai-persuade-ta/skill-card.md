## Description:

旅行提案生成器，帮用户生成一份用真实数据说服伴侣/老板/爸妈/朋友的旅行方案。调用FlyAI获取机票酒店景点真实价格，针对性击破顾虑，可直接转发微信。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to gather travel details, compare costs, and generate Chinese persuasion proposals for partners, managers, parents, or friends. The skill can produce shareable text and an optional HTML proposal grounded in FlyAI travel search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents global installation of the latest FlyAI CLI package, including a sudo fallback.

Mitigation: Verify the FlyAI package identity and intended version before installation, and prefer a least-privilege Node environment such as nvm over sudo.

Risk: The skill documents disabling TLS certificate validation for FlyAI travel searches.

Mitigation: Use normal TLS validation for routine searches and only investigate certificate failures through trusted network and package channels.

Risk: The skill can persist user travel profile details across sessions.

Mitigation: Save profile data only after explicit user confirmation and include only information the user is comfortable retaining.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-persuade-ta)
- [FlyAI command reference](artifact/reference/flyai-commands.md)
- [Persuasion templates](artifact/reference/persuasion-templates.md)
- [Scenario templates](artifact/reference/scenario-templates.md)
- [User profile storage](artifact/reference/user-profile-storage.md)
- [Flight search reference](artifact/reference/references/search-flight.md)
- [Hotel search reference](artifact/reference/references/search-hotel.md)
- [POI search reference](artifact/reference/references/search-poi.md)
- [Keyword search reference](artifact/reference/references/keyword-search.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Chinese Markdown-style proposal text with optional HTML file output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include travel prices, itinerary details, objection-handling copy, and user profile updates when the user confirms persistence.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
