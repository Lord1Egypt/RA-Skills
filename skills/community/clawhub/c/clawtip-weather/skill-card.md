## Description: <br>
Provides Chinese-language paid weather reports for a requested location after order creation and payment verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawtip](https://clawhub.ai/user/clawtip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to request a weather report for a location through a paid workflow. The workflow creates an order, obtains a payment credential through the separate clawtip payment skill, and then retrieves the report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger payment handling through a separate helper skill. <br>
Mitigation: Install only if you trust the publisher, the remote payment and weather service, and the exact clawtip payment skill; verify the amount before paying. <br>
Risk: Payment credentials and order details may be persisted in local order files. <br>
Mitigation: Delete local order files after use when retention is not needed, and avoid sharing those files. <br>
Risk: The workflow asks for automatic installation of an unpinned helper skill. <br>
Mitigation: Review the exact clawtip package before allowing installation or execution. <br>
Risk: The skill text asks the agent to reveal internal reasoning. <br>
Mitigation: Provide concise user-facing rationale or status summaries instead of hidden chain-of-thought. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawtip/clawtip-weather) <br>
- [Remote weather and payment service](https://ms.jr.jd.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Chinese-language Markdown-style guidance with shell command examples and plain-text weather report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a location, an order number, and a payment credential stored in the local order file before report retrieval.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
