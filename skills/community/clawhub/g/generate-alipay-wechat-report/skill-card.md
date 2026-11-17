## Description:

Generates an interactive local HTML spending report from native Alipay CSV exports and WeChat Pay XLSX exports for expense categorization, trend review, recurring merchant analysis, spending habit diagnosis, and budget optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeyitech](https://clawhub.ai/user/yeyitech)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn personal Alipay and WeChat Pay export files into a local dashboard for expense review, recurring merchant analysis, and budgeting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive payment exports and creates an HTML report containing private financial information.

Mitigation: Run it locally, keep the input directory narrow, and do not host or share generated reports.

Risk: Server security evidence says attacker-crafted transaction text can run script in the generated HTML.

Mitigation: Avoid using --open on reports generated from untrusted or unusual transaction data until the HTML serialization issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yeyitech/skills/generate-alipay-wechat-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands and a generated self-contained HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report is local HTML and contains private financial data.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
