## Description:

帝王纪年转换 / Emperor Year Converter converts between Chinese imperial reign years and CE/BCE dates, searches dynasties, emperors, reign names, and historical years, and covers 790 reign periods from 878 BCE to 1911 CE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and historical researchers use this skill to answer natural-language questions about Chinese reign years, convert between reign-year notation and CE/BCE years, and search or list reign periods by dynasty, emperor, or reign name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode can read an input file and write conversion results to a specified output path.

Mitigation: Use batch mode only with files and output paths chosen by the user.

Risk: Historical conversion results are limited to the bundled Chinese reign-period dataset and do not cover Japanese, Korean, Vietnamese, or post-1911 reign years.

Mitigation: Check the stated coverage range and ask for clarification when a query falls outside Chinese reign periods from 878 BCE to 1911 CE.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjefferson/skills/emperor-year-converter)
- [ClawHub publisher profile](https://clawhub.ai/user/tjefferson)
- [Emperor reign data source](https://hanzi.unihan.com.cn/Emperor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command examples and tabular conversion results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include multiple matching reign periods for transition years or shared reign names; batch mode can write conversion output to a user-specified file.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
