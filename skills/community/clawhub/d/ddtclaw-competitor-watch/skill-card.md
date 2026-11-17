## Description:

用已发布的餐饮品牌门店快照，快速回答开关店、区域扩张、竞对方向、销售攻店与选址初筛。适合市场、拓展和销售团队在一次对话中形成可执行判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Market, expansion, and sales teams use this skill to analyze published restaurant brand store snapshots, compare competitors, assess regional growth or contraction, and screen candidate locations. It emphasizes aggregate facts first and limits store-level detail to explicit user requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brand, address, landmark, and candidate-location queries may be sent to gotoshop-ai.com.

Mitigation: Use the skill only when sharing those queries with the service is acceptable, and avoid sending confidential expansion plans or sensitive location lists unless approved.

Risk: DDT_API_KEY grants access to the external API if exposed.

Mitigation: Store the key only in local environment variables, do not paste it into prompts or outputs, and rotate it if disclosure is suspected.

Risk: Store-opening observations, closure confirmations, nearby searches, and site-screening results have explicit coverage and interpretation limits.

Mitigation: Report coverage periods and data definitions, use aggregate endpoints first, and avoid presenting the results as official openings, official closures, revenue, profit, AUV, or probability of success.

## Reference(s):

- [店店通餐饮开关店与竞对分析](https://gotoshop-ai.com/ddtclaw/)
- [店店通 API Key setup](https://gotoshop-ai.com/ddtclaw/open)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Analysis]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, limited requested details, and occasional bash or curl snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should omit API keys, internal identifiers, table names, supplier names, version UUIDs, and unsupported business claims.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
