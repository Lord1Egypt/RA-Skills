## Description:

抖音公开数据只读：关键词搜视频/图文、用户/达人搜索、博主作品、作品详情、评论、热榜；可做公域获客/竞品截流（search→comment）与需求挖掘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT-0

## Use Case:

Short video operators, marketers, and analysts use this skill to search and inspect public Douyin videos, accounts, comments, and trends, then analyze competitors, audience sentiment, demand, and content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links or IDs are sent to guaikei.com when requests run; users may not expect this third-party data transfer.

Mitigation: Explain the transfer before running a query, send only the public keyword or link needed for the requested lookup, and keep the API token private.

## Reference(s):

- [Douyin data service and token support](https://www.guaikei.com)
- [Publisher profile: um-why](https://clawhub.ai/user/um-why)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Customer acquisition guide](artifact/references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON records with concise analytical guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are written as JSON to stdout and saved under logs/ for supported queries; live hot-list results are not saved.]

## Skill Version(s):

1.5.0 (source: server-resolved release evidence, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
