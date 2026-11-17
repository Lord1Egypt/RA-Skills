## Description:

跨境多国税务速查支持用国家名或自然语言查询30多个国家和地区的税率、申报周期、注册门槛、特殊规则以及EU OSS/IOSS方案，并生成交互式HTML税务速查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border ecommerce sellers, operators, and tax or compliance staff use this skill to quickly compare VAT, GST, sales-tax rates, registration thresholds, filing cycles, and EU OSS/IOSS considerations across major markets. Its output should be treated as reference material rather than tax or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tax data may be incorrect or outdated and does not constitute tax or legal advice.

Mitigation: Use generated reports only as reference material and verify decisions against official tax authorities or a qualified adviser.

Risk: The skill may activate on broad tax terms and write persistent HTML reports in the user's home directory.

Mitigation: Review trigger terms before deployment and run the script only for intentional tax lookup tasks.

Risk: HTML reports can contain unescaped user-supplied query text.

Mitigation: Avoid untrusted queries until output escaping is fixed, or sanitize query text before rendering HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/cross-border-tax)
- [bettermen publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Interactive HTML report files with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent HTML reports under ~/.workbuddy/skills/cross-border-tax/output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
