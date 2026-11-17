## Description:

公共资源交易信息收集 helps an agent collect project announcements from the Zibo public-resource trading website for a specified date range and export the results to Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n1ke9yd](https://clawhub.ai/user/n1ke9yd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect project location, project name, and publication date records for Zibo public-resource trading notices, then save the collected list as an Excel spreadsheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Excel export may overwrite an existing local file if the same path is reused.

Mitigation: Choose an explicit output path and confirm it does not replace a file you need before running the export.

Risk: The skill may use a connected browser profile while visiting the target public website.

Mitigation: Use a separate browser profile when you do not want the agent operating in an existing Chrome session.

Risk: Incomplete page loads or incorrect date filtering can produce missing or out-of-range records.

Mitigation: Wait for each page to load and verify publication dates before exporting the collected list.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n1ke9yd/skills/ggzy-collect)
- [Zibo public-resource trading website](http://ggzyjy.zibo.gov.cn:8082/)
- [Zibo construction-engineering public-resource listing](http://ggzyjy.zibo.gov.cn:8082/jyxx/002001/gonggongziyuan.html?Paging=1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript or shell command snippets and an Excel file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local Excel file at a user-selected output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
