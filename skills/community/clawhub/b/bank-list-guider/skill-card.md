## Description: <br>
Helps users query the treasury management system's supported bank list, check whether a specific bank is supported, and understand bank access status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SongsongJiang](https://clawhub.ai/user/SongsongJiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-facing support, sales, and implementation teams use this skill to answer questions about which banks are supported by a treasury management system and to provide access-status details for a specific bank. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The supported-bank list may become outdated as bank access changes. <br>
Mitigation: Review and update references/banks.md whenever banks are added, removed, or their access status changes. <br>
Risk: The skill may provide unsupported-bank answers that users could treat as final product commitments. <br>
Mitigation: For banks not listed in references/banks.md, record the request and route it to the product or implementation team before promising support. <br>
Risk: Bank availability and access notes are business-sensitive operational data. <br>
Mitigation: Grant only the files and tools needed for the bank-list task and confirm the artifact content is appropriate for the intended audience before deployment. <br>


## Reference(s): <br>
- [Bank List Guider on ClawHub](https://clawhub.ai/SongsongJiang/bank-list-guider) <br>
- [Publisher profile: SongsongJiang](https://clawhub.ai/user/SongsongJiang) <br>
- [references/banks.md](references/banks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown tables and short natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are grounded in references/banks.md and may include grouped bank lists, support status, and access notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
