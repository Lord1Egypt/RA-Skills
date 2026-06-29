## Description: <br>
Операционный директор для работы компании с банком: сводка и статус по счёту, ограничения, картотека, сертификаты, доверенности и рекомендованные действия через JSON-инструмент и виджет карточки счёта. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikhail2018](https://clawhub.ai/user/mikhail2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and company staff use this skill to ask about a company bank account status, recent payments, blocked or suspended operations, card-file queues, signature certificates, powers of attorney, and next operational steps. It is intended for Russian-language banking operations workflows that need short summaries and status-oriented guidance. <br>

### Deployment Geography for Use: <br>
Russia <br>

## Known Risks and Mitigations: <br>
Risk: Banking-status summaries may expose sensitive account information in chat, widget views, or repeated daily summaries. <br>
Mitigation: Install and schedule the skill only in appropriate workspaces, review who can see the chat and Widgets page, and treat generated account summaries as sensitive business information. <br>
Risk: The bundled account data is synthetic unless the skill is later connected to a real bank source. <br>
Mitigation: Confirm the data source before making operational decisions and disclose when responses are based on synthetic or demonstration data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikhail2018/bank-ops-director-api) <br>
- [Sber Business: account arrests, collections, and suspensions](https://www.sberbank.ru/ru/s_m_business/bankingservice/arest) <br>
- [Sber Business: electronic signature](https://www.sberbank.ru/ru/s_m_business/nbs/signature) <br>
- [Sber Business: certificates and statements](https://www.sberbank.ru/ru/s_m_business/rko/tariffs/spravki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Concise chat responses, JSON account-status data, and an inline account-status widget] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses date-relative synthetic account data unless connected to a real bank data source.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
