## Description: <br>
Операционный директор для работы компании с банком: сводка и статус по счёту (остаток, обороты, последние операции), приостановления и блокировки (115-ФЗ, ст. 76 НК), картотека, сертификаты ЭП/ЭЦП, доверенности и рекомендованные действия (по запросу). Данные счёта возвращает локальный скрипт (JSON). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikhail2018](https://clawhub.ai/user/mikhail2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to check a company's bank account status, balances, turnover, recent operations, restrictions, payment queues, electronic signature certificates, powers of attorney, and recommended next actions from local JSON data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring account summaries can expose sensitive financial information in chat logs or shared workspaces. <br>
Mitigation: Enable daily summaries only after confirming the destination, included fields, redaction needs, and how to disable the schedule. <br>
Risk: Banking procedures and legal references may be incomplete or stale if official sources are unavailable. <br>
Mitigation: Use official bank or legal sources when available and treat built-in procedure notes as orientation rather than legal advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikhail2018/bank-ops-director-script) <br>
- [Sberbank arrests, collections, and account suspensions](https://www.sberbank.ru/ru/s_m_business/bankingservice/arest) <br>
- [Sberbank electronic signature](https://www.sberbank.ru/ru/s_m_business/nbs/signature) <br>
- [Sberbank account certificates](https://www.sberbank.ru/ru/s_m_business/rko/tariffs/spravki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown narrative based on JSON returned by a local Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses synthetic local account data generated from scripts/get_account.py; scheduled summaries may expose financial information in chat logs or shared workspaces.] <br>

## Skill Version(s): <br>
0.3.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
