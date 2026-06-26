## Description: <br>
Automates Audtools ecommerce category collection from CSV category links, including login, task submission, tab management, and optional bulk export actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QirongZhang](https://clawhub.ai/user/QirongZhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers managing Audtools collection workflows use this skill to validate CSV category-link inputs, submit ecommerce collection tasks, and optionally trigger export of collected product records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release embeds shared Audtools login credentials. <br>
Mitigation: Remove the embedded credentials, rotate any exposed account secrets, and require user-provided credentials through a secure local mechanism before installation. <br>
Risk: The skill can perform bulk export actions without clear user-controlled scoping. <br>
Mitigation: Before running exports, confirm the account in use, the exact records selected, and the destination or handling of exported files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QirongZhang/ecommerce-category-collector) <br>
- [Publisher profile](https://clawhub.ai/user/QirongZhang) <br>
- [CSV format reference](references/csv-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes CSV files with a required complete-link column and can run against a single CSV file or a directory of CSV files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
