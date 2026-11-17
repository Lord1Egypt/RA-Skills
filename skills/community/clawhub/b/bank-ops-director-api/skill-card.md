## Description:

Операционный директор для работы компании с банком: сводка и статус по счёту, приостановления и блокировки, картотека, сертификаты ЭП/ЭЦП, доверенности и рекомендованные действия через JSON-инструмент `bank_get_status` и карточку счёта на странице Widgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikhail2018](https://clawhub.ai/user/mikhail2018)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operators use this skill to ask about a company bank account, including balances, recent operations, payment failures, restrictions, card-index items, signature certificates, powers of attorney, and first recommended actions. The skill also exposes a widget card for a compact account status view.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can show realistic, current-dated synthetic account data without making the demo nature clear.

Mitigation: Show a persistent demo-data warning in every chat and widget response before users rely on balances, payment status, restrictions, certificates, or recommended actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikhail2018/skills/bank-ops-director-api)
- [Sberbank business account arrests and suspensions](https://www.sberbank.ru/ru/s_m_business/bankingservice/arest)
- [Sberbank business electronic signature](https://www.sberbank.ru/ru/s_m_business/nbs/signature)
- [Sberbank business certificates and account references](https://www.sberbank.ru/ru/s_m_business/rko/tariffs/spravki)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown chat responses plus JSON tool and widget payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses locally generated synthetic sample banking data; no real bank integration is evidenced.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
