## Description: <br>
Funpay Assistant automates common FunPay chat replies, monitors buyer messages, notifies the operator about account-login consent, and forwards unrecognized messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirra87654321](https://clawhub.ai/user/mirra87654321) <br>

### License/Terms of Use: <br>


## Use Case: <br>
FunPay sellers or operators use this skill to monitor buyer chats and handle routine availability, region, VPN, and account-access messages. Review the release before any customer-facing use because the security evidence flags credentials, private chat history, and automatic messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships with an embedded FunPay credential. <br>
Mitigation: Remove the embedded key, rotate the exposed credential, and require operators to provide credentials through a secure runtime secret. <br>
Risk: The bundled state file contains private chat history. <br>
Mitigation: Delete bundled chat state before distribution or deployment and start from an empty local state file. <br>
Risk: The script can send customer-facing replies and request buyer account access without prior operator review. <br>
Mitigation: Require explicit operator approval before sending replies or asking buyers to allow account access. <br>
Risk: Runtime dependencies are not declared or verified in the release evidence. <br>
Mitigation: Declare required dependencies and verify their source and versions before running the script. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python script behavior and plain-text notification output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send FunPay chat messages and print operator notifications when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
