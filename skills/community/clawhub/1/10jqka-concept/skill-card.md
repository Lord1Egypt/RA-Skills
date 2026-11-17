## Description:

Queries Tonghuashun/iWencai for Chinese A-share stock concept-board information by using public Tonghuashun F10 pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to look up A-share concept boards, concept constituents, and concept-board market data for stock-analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock codes and concept names are sent to Tonghuashun/iWencai services during lookup.

Mitigation: Use the skill only with data appropriate for those services and disclose the outbound requests in deployment environments.

Risk: The batch script writes a local cache under ~/.openclaw/workspace/memory/cache, which can persist queried stock data on shared systems.

Mitigation: Run in a dedicated Python environment and clear or restrict the cache directory when working on shared hosts.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Review and pin dependency versions such as requests, beautifulsoup4, and lxml before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liweijie0709-cmyk/skills/10jqka-concept)
- [Tonghuashun F10 data source](https://basic.10jqka.com.cn/)
- [Tonghuashun concept page format](https://basic.10jqka.com.cn/{股票代码}/concept.html)
- [Tonghuashun concept board pages](https://q.10jqka.com.cn/gn/index/field/199112/order/asc/page/1/prep/1/quote/{concept_name})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with Python, shell command, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts return stock codes, stock names, concept lists, counts, cache metadata, and error messages when requests or parsing fail.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
