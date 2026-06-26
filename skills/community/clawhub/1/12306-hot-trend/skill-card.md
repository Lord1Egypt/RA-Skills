## Description: <br>
Provides agent guidance for official 12306 railway travel workflows, including ticket availability checks, standby monitoring, and order summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to assist with compliant personal 12306 railway travel tasks such as checking ticket availability, monitoring standby status, organizing orders, and preparing concise travel summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may assist with sensitive 12306 account workflows such as login, standby submission, payment-related steps, cancellation, refunds, exports, or reminder setup. <br>
Mitigation: Require explicit user confirmation before any sensitive account or ticketing action. <br>
Risk: Travel workflows can expose passenger names, order numbers, and identity-document fragments. <br>
Mitigation: Retain only the minimum summary needed for reminders or exports and avoid storing passenger names, full order numbers, or ID fragments longer than necessary. <br>
Risk: High-frequency queries or attempts to bypass human verification can trigger platform controls or violate 12306 rules. <br>
Mitigation: Use only official 12306 pages, do not bypass CAPTCHA or human checks, and rate-limit polling as described by the skill. <br>


## Reference(s): <br>
- [12306 Official Website](https://www.12306.cn/) <br>
- [12306 Ticket Booking](https://kyfw.12306.cn/otn/leftTicket/init) <br>
- [12306 Standby Ticketing](https://kyfw.12306.cn/otn/subscribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ticket availability lists, standby status summaries, reminders, and CSV-oriented order summary guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
