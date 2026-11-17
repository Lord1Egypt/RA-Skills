## Description:

Gerencia finanças pessoais do Evandro com registro por categorias em linguagem natural, processamento de extratos e faturas, e resumos mensais e anuais.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evandrotho](https://clawhub.ai/user/evandrotho)

### License/Terms of Use:

MIT-0

## Use Case:

Private personal-finance users use this skill to guide an agent through recording income and expenses, processing bank statements and card bills, preventing duplicate entries, and producing monthly or annual summaries. It is tailored to Evandro's finance workspace and should be adapted before reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains real personal-finance context and named personal relationships.

Mitigation: Keep it limited to the intended private workspace and remove real names, relationships, and amounts before sharing or reuse.

Risk: Broad finance triggers could activate around sensitive records or unrelated files.

Mitigation: Narrow activation to explicit finance commands and review any requested file reads or updates before execution.

Risk: Incorrect statement parsing or duplicate detection could create misleading finance records.

Mitigation: Require user confirmation before writes, check for duplicates by value and date, and preserve the source transaction description.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evandrotho/skills/financas-donna)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown financial tables and concise Portuguese confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update monthly and annual finance Markdown files after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
