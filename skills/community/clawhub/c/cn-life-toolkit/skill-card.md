## Description:

中国生活服务工具包，支持天气查询（街道级）、限行提醒、油价查询、快递物流跟踪、公交换乘查询等日常生活服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users in or traveling within China use this skill to ask an agent for weather, vehicle restriction, fuel price, parcel tracking, and public transit guidance for daily-life decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may include parcel numbers, exact addresses, travel routes, or other location-linked details.

Mitigation: Share only the minimum information needed for the lookup and avoid exposing sensitive personal or delivery details.

Risk: Weather, courier, traffic, fuel price, and transit answers may depend on third-party services or public notices that can be delayed or change quickly.

Mitigation: Confirm time-sensitive results against official or primary service sources before making travel, driving, or delivery decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/cn-life-toolkit)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted natural-language responses with local-service lookup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include weather, traffic restriction, fuel price, parcel, transit, and location-linked details from third-party or public sources.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
