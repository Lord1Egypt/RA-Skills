## Description:

使用百度地图地址文本进行餐饮品牌竞对情报分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External market, competitive-intelligence, and sales teams use this skill to analyze published restaurant brand store snapshots, compare network changes, identify priority regions, and screen nearby stores or candidate sites from Baidu Maps address text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows an inherited endpoint variable to receive the user's bearer API key without validation.

Mitigation: Set DDT_OPEN_BASE explicitly to the official gotoshop-ai.com/ddtclaw endpoint before use, avoid shared environments where that variable may be pre-set, and keep DDT_API_KEY scoped and rotated if misused.

Risk: The release security verdict is suspicious despite no individual risk findings being listed.

Mitigation: Install only after trusting the publisher and service, and review the skill before using it in sensitive environments.

## Reference(s):

- [店店通 DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill release page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-restaurant-competitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise analysis, metrics, coverage notes, limited detail rows, and optional bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses published restaurant store snapshots and avoids full store-list export or unsupported business conclusions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
