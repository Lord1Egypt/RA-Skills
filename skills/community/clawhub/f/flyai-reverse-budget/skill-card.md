## Description:

反向穷游助手，我有X元能去哪？输入总预算、出发城市、可出行天数，AI反向搜索所有可能性，生成3档方案（省钱极限版/舒适版/极限拉满版），每档含完整预算拆解。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to answer budget-first trip planning questions, such as where they can go from a given departure city for a fixed budget and duration. It compares transport, lodging, attractions, meals, and local transport into three budget tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe network and install practices, including guidance that can disable TLS verification or install an unpinned global CLI.

Mitigation: Keep TLS verification enabled, use a verified pinned FlyAI CLI in an isolated environment, and avoid sudo or global @latest installs unless separately reviewed.

Risk: The skill can persist travel preferences and profile data through memory tools or a local profile file.

Mitigation: Make profile storage opt-in, show users what will be saved, and provide a clear way to inspect, update, and delete saved travel data.

Risk: Travel prices, availability, and booking links may change after the agent produces a plan.

Mitigation: Label price-sensitive recommendations as current estimates and require users to verify final prices and terms before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hello-ahang/skills/flyai-reverse-budget)
- [Workflow](reference/workflow.md)
- [Tools](reference/tools.md)
- [User profile storage](reference/user-profile-storage.md)
- [Examples](reference/examples.md)
- [AI search](reference/ai-search.md)
- [Keyword search](reference/keyword-search.md)
- [Flight search](reference/search-flight.md)
- [Hotel search](reference/search-hotel.md)
- [Marriott hotel search](reference/search-marriott-hotel.md)
- [Marriott package search](reference/search-marriott-package.md)
- [POI search](reference/search-poi.md)
- [Train search](reference/search-train.md)
- [Self learning](reference/self-learning.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel recommendations with budget breakdowns, comparison tables, booking links, and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in live travel search results when available and may include user preference updates after confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
