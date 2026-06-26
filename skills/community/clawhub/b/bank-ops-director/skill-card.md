## Description: <br>
Операционный директор для работы компании с банком: сводка и статус по счёту, приостановления и блокировки, картотека, сертификаты ЭП/ЭЦП, банк-клиент, доверенности и рекомендованные действия. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikhail2018](https://clawhub.ai/user/mikhail2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations staff use this skill to review demo company banking status, explain account restrictions, check payment and document status, and prepare next-step guidance for bank operations questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake embedded demo account data for live bank information. <br>
Mitigation: Require the skill to disclose that account status comes from embedded demo data unless a real bank lookup is clearly performed. <br>
Risk: Simulated API phrasing can make responses appear connected to a real bank system. <br>
Mitigation: Remove or rewrite simulated bank API language unless the agent is actually using an authenticated bank integration. <br>
Risk: Vague prompts about banking status may receive overconfident answers. <br>
Mitigation: Ask a clarifying question when the user request is ambiguous or when the requested account, period, bank, or document is not present in the dataset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikhail2018/bank-ops-director) <br>
- [Publisher profile](https://clawhub.ai/user/mikhail2018) <br>
- [Sberbank: arrests, collections, and account suspensions](https://www.sberbank.ru/ru/s_m_business/bankingservice/arest) <br>
- [Sberbank: electronic signature](https://www.sberbank.ru/ru/s_m_business/nbs/signature) <br>
- [Sberbank: certificates and statements](https://www.sberbank.ru/ru/s_m_business/rko/tariffs/spravki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with short status summaries, checklists, and source links when procedure guidance is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calculated dates, amounts, document statuses, and scheduled-summary guidance based on the embedded demo banking dataset.] <br>

## Skill Version(s): <br>
0.9.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
