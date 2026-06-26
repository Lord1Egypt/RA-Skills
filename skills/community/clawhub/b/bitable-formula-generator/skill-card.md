## Description: <br>
Generates Feishu Bitable-compatible formulas from Excel-style logic and can write them to Bitable formula fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengfen1987](https://clawhub.ai/user/chengfen1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to inspect Feishu Bitable tables, generate compatible formulas from business logic, and create or update formula fields after validating field names and dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials and Bitable tokens can allow access to table metadata and formula-field updates. <br>
Mitigation: Use a least-privilege Feishu app, keep FEISHU_APP_ID and FEISHU_APP_SECRET out of chats, logs, and repositories, and confirm the target app token, table, field, and formula before execution. <br>
Risk: A generated or applied formula can overwrite an existing formula field or produce incorrect results when dependent fields, option values, or intermediate formulas are wrong. <br>
Mitigation: Inspect tables and fields first, verify intermediate formula fields and actual option values, and review the generated formula before using set-formula or manually pasting it. <br>
Risk: Shell parsing can truncate formulas that contain special characters such as <, >, |, or &. <br>
Mitigation: Use a script-file or direct API request path for formulas with shell-sensitive characters instead of passing them directly as command-line arguments. <br>


## Reference(s): <br>
- [Bitable function and Excel mapping reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/chengfen1987/bitable-formula-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with formulas, explanations, command examples, and optional JavaScript or API request snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu Bitable formula expressions and commands that read table metadata or create and update formula fields.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
