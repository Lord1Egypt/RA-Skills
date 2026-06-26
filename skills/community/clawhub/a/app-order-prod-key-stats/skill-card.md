## Description: <br>
Computes key JiuShi Sports app order metrics by order title or order detail, with optional keyword and business-section filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaggerliu](https://clawhub.ai/user/jaggerliu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Authorized business analysts and operations teams use this skill to query production order data for order counts, unpaid and refund counts, payment and refund amounts, and user counts over a specified time range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries production business order data using locally supplied database credentials. <br>
Mitigation: Use it only with authorization to access the JiuShi order database, and configure a narrowly scoped read-only account. <br>
Risk: The SQL template builds filters from user input without strong input controls. <br>
Mitigation: Replace f-string SQL with parameterized queries and strict allowlists for dates, dimensions, keywords, and business sections before production use. <br>
Risk: Database credentials or connection details could be exposed through careless execution or logging. <br>
Mitigation: Provide credentials through protected environment variables and avoid printing passwords or full connection strings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaggerliu/app-order-prod-key-stats) <br>
- [Publisher profile](https://clawhub.ai/user/jaggerliu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown tables and Chinese summary text, with Python query code when execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized database credentials and Python packages mysql-connector-python, pandas, and tabulate.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
