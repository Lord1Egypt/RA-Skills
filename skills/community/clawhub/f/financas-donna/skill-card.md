## Description: <br>
Gerencia finanças pessoais do Evandro com registro por categorias via linguagem natural, processamento de extratos e faturas, e resumos mensais e anuais. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evandrotho](https://clawhub.ai/user/evandrotho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using Evandro's finance workspace use this skill to record income and expenses, process bank statements and card invoices, prevent duplicate entries, and generate monthly or annual finance summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update sensitive personal finance files. <br>
Mitigation: Use it only in the intended finance workspace, keep backups, and require explicit confirmation before any finance file is read or changed. <br>
Risk: Broad finance-related trigger words may activate the skill when the user did not intend to manage finance records. <br>
Mitigation: Narrow activation triggers when possible and ask the user to confirm financial intent before processing files or recording transactions. <br>
Risk: The artifact contains personal finance rules specific to Evandro and related people. <br>
Mitigation: Install it only for Evandro's own workflow or replace the personal context with the user's own rules before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evandrotho/financas-donna) <br>
- [Publisher profile](https://clawhub.ai/user/evandrotho) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions, confirmation prompts, tabular finance summaries, and file update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update finance Markdown files in a workspace after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
