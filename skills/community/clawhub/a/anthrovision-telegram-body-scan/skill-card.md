## Description: <br>
Run end-to-end body-scan measurement flow in Telegram using AnthroVision bridge tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dr2101](https://clawhub.ai/user/dr2101) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to collect body measurements from a consenting person's Telegram video through the AnthroVision bridge workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Body-scan videos and derived measurements are sensitive personal data. <br>
Mitigation: Process only videos from people who have explicitly consented to the AnthroVision bridge workflow. <br>
Risk: Unsafe video inputs could reference local files or private network locations. <br>
Mitigation: Accept only video attachments or downloadable HTTPS video URLs, and reject local paths, localhost, loopback, and private-subnet URLs. <br>
Risk: Upstream tool output could include arbitrary or untrusted text. <br>
Mitigation: Return deterministic messages from structured fields only, without relaying arbitrary tool strings, links, or commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dr2101/anthrovision-telegram-body-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown text with fixed-format scan status and measurement summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured fields for scan_id, status, measurements, and waist-to-hip summary; avoids links, commands, and untrusted upstream text.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
