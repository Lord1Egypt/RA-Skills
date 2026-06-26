## Description: <br>
BaZi Insight Report helps agents create paid Cantian AI BaZi report checkout links and check report generation or download status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianlinle](https://clawhub.ai/user/tianlinle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill through an agent to order Cantian AI BaZi reports, receive payment links, and check whether a paid report is ready to download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checkout flow sends personal contact and birth details to Cantian AI. <br>
Mitigation: Collect only the required fields, tell users what will be sent, and proceed only when they are comfortable sharing the information. <br>
Risk: The skill creates paid report checkout links. <br>
Mitigation: Ask users to review the generated order details and payment page before paying, and regenerate the checkout link if details are wrong. <br>
Risk: Returned profile IDs can be used to check report status. <br>
Mitigation: Keep profile IDs private and share download or status details only with the user who requested the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianlinle/bazi-report) <br>
- [Cantian AI](https://cantian.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment links, profile IDs, payment status, report readiness, and download page URLs.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
