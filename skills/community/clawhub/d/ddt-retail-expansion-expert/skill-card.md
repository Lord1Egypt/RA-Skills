## Description:

零售连锁拓店选址专家，分析品牌门店规模、区域层级、业态结构、周边画像与候选点竞争。适用于拓展经理、选址团队和区域负责人筛选机会城市、比较地址或判断覆盖空白。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Retail expansion managers, site-selection teams, and regional operators use this skill to screen opportunity markets, compare candidate locations, inspect brand coverage gaps, and summarize retail competitive context from the disclosed DDT API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retail brand queries, user-provided coordinates, and public store IDs may be sent to the disclosed DDT API.

Mitigation: Use the skill only when that data sharing is acceptable for the user and organization; avoid submitting unnecessary precise coordinates or store identifiers.

Risk: The skill requires an API key for authenticated requests.

Mitigation: Keep the key in the runtime environment and do not paste it into chat, logs, repositories, or generated output.

Risk: Snapshot and preview data can be mistaken for trends, complete market lists, or success predictions.

Mitigation: Report coverage and data-version limits, treat missing coverage as unavailable rather than zero, and require site-level validation before business decisions.

## Reference(s):

- [DDT retail API homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage and data-version notes, and limited store details when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current retail snapshot data and constrained previews; does not output API keys, internal identifiers, supplier fields, or raw English enum values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
