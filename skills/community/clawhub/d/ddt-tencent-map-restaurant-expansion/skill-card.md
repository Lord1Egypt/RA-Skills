## Description:

餐饮拓店机会区域、候选地址竞争与现场验证优先级分析，可将腾讯地图中复制出的地点名称和地址文本作为地点输入，基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to analyze restaurant chain expansion opportunities, nearby competition, risk gaps, and field verification priorities from Tencent Map address text and GotoShop/DDT published store snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends restaurant names, locations, and address queries to the GotoShop/DDT API.

Mitigation: Install only if that third-party API use is acceptable for the intended workflow and data handling policy.

Risk: The API key could be exposed if copied into prompts, logs, or generated output.

Mitigation: Store the key only in the local environment variable and avoid displaying it in agent responses.

Risk: Generated site-selection analysis is based on a published data snapshot and is not official Tencent Map or brand data.

Mitigation: Treat conclusions as a decision-support snapshot and verify important locations, coverage periods, and business assumptions before action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-restaurant-expansion)
- [GotoShop/DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [GotoShop/DDT API key setup](https://gotoshop-ai.com/ddtclaw/open)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with concise metrics, coverage notes, bounded details, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bounded API result previews and should not expose API keys, internal identifiers, table names, vendor names, or version UUIDs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
