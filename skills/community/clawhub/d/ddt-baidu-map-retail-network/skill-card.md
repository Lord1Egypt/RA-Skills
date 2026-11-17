## Description:

零售品牌门店规模、业态结构、区域覆盖与候选点机会分析；可将百度地图中复制出的地点名称和地址文本作为地点输入，并基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze published retail-brand store networks, including scale, regional coverage, category mix, surrounding context, brand comparisons, and candidate-site screening from explicit address or coordinate inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis requests may send brand names, copied address text, coordinates, and the DDT API key to the configured DDT service.

Mitigation: Use the default or another trusted DDT base URL, keep DDT_API_KEY in environment variables only, and avoid exposing the key in chat, logs, or version control.

Risk: Users may mistake the skill for an official Baidu Maps product or infer a Baidu Maps data relationship.

Mitigation: State that the skill is not an official Baidu Maps product and that conclusions come from the published DDT retail-store snapshot.

Risk: Store-network outputs can be incomplete or misleading when coverage is missing, previews are truncated, or a brand is not published.

Mitigation: Check API ok status, coverage fields, data version, and preview.truncated before making business conclusions; mark unavailable coverage explicitly instead of treating missing values as zero.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-retail-network)
- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [Publisher profile](https://clawhub.ai/user/horacetu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise retail-network conclusions, key metrics, coverage notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses published retail snapshots and limited store previews; does not output API keys, internal identifiers, supplier fields, or unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
