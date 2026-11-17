## Description:

Операционный директор для работы компании с банком: сводка и статус по счёту (остаток, обороты, последние операции), приостановления и блокировки (115-ФЗ, ст. 76 НК, арест), картотека, сертификаты ЭП/ЭЦП и банк-клиент (ДБО), доверенности и рекомендованные действия (по запросу). Ежедневная сводка по расписанию.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikhail2018](https://clawhub.ai/user/mikhail2018)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operators use this Russian-language skill to get concise account summaries, review bank-operation restrictions, check card-index items, certificates, powers of attorney, and request next actions for a company bank account. The skill is grounded in embedded demo banking data and can optionally schedule a daily account summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present static embedded account balances, operations, restrictions, certificates, and recommendations as if they came from a live bank API.

Mitigation: Label embedded data as demo data unless the skill is changed to use an authenticated bank integration.

Risk: The instruction allows an API-simulation phrase that can make demo responses look operationally authoritative.

Mitigation: Remove the API-simulation wording or replace it with an explicit source label before deployment.

Risk: Broad trigger phrases could route unrelated banking questions to this company-specific skill.

Mitigation: Require confirmation that the user is asking about the configured company bank account before using embedded account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikhail2018/skills/bank-ops-director)
- [Sberbank: arrests, collections, and account suspension](https://www.sberbank.ru/ru/s_m_business/bankingservice/arest)
- [Sberbank: electronic signature](https://www.sberbank.ru/ru/s_m_business/nbs/signature)
- [Sberbank: certificates and statements](https://www.sberbank.ru/ru/s_m_business/rko/tariffs/spravki)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, Configuration]

**Output Format:** [Markdown and plain text responses with account summaries, checklists, recommendations, source links, and scheduling instructions when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish embedded demo data from live bank information and should cite official sources for procedural guidance when web access is used.]

## Skill Version(s):

0.9.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
