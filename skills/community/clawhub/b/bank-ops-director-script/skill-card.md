## Description:

Операционный директор для работы компании с банком: сводка и статус по счёту (остаток, обороты, последние операции), приостановления и блокировки (115-ФЗ, ст. 76 НК), картотека, сертификаты ЭП/ЭЦП, доверенности и рекомендованные действия (по запросу).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikhail2018](https://clawhub.ai/user/mikhail2018)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or business operators use this skill to summarize a company's bank-account status from local JSON data, including balance, turnover, payment restrictions, card-file items, certificates, powers of attorney, and next recommended actions. The skill is written for Russian-language banking operations and can also draft daily account summaries when scheduling is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthetic banking data may be mistaken for live account balances, restrictions, payment statuses, or scheduled reports.

Mitigation: Clearly label every account response and recurring summary as synthetic demonstration data unless the skill is changed to use verified bank data.

Risk: Recommended actions may influence financial, tax, or legal decisions.

Mitigation: Base procedure guidance on official bank sources and require legal or finance review before acting on account restrictions, card-file items, certificates, or powers of attorney.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikhail2018/skills/bank-ops-director-script)
- [Sber: arrests, collections, and account suspensions](https://www.sberbank.ru/ru/s_m_business/bankingservice/arest)
- [Sber: electronic signature](https://www.sberbank.ru/ru/s_m_business/nbs/signature)
- [Sber: business account certificates](https://www.sberbank.ru/ru/s_m_business/rko/tariffs/spravki)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Russian prose or Markdown summaries backed by local JSON returned from the Python helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper accepts a section argument: all, account, operations, restrictions, kartoteka, certificates, powers_of_attorney, or recommended_actions.]

## Skill Version(s):

0.3.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
