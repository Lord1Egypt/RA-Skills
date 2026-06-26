## Description: <br>
Generates a daily Chinese anti-fraud briefing by searching domestic bank and payment institution news for cases, involved banks, amounts, and related details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdl2005](https://clawhub.ai/user/wdl2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fraud monitoring and financial operations teams use this skill to prepare daily briefings on Chinese domestic bank and payment-institution anti-fraud incidents for Feishu distribution. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled reporting or Feishu posting could send the briefing to an unintended destination if configured incorrectly. <br>
Mitigation: Confirm the cron schedule and use a narrowly scoped Feishu webhook or destination before enabling the workflow. <br>
Risk: Search queries or report context could expose internal incident details, customer data, secrets, or sensitive monitoring interests to external services. <br>
Mitigation: Limit queries and inputs to public anti-fraud news and exclude internal data, customer data, secrets, and sensitive monitoring interests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown numbered report with optional shell search command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured case entries include incident date, case process, bank name, amount, and other relevant information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
