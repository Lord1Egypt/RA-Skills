## Description: <br>
AI Safety Guard is a lightweight OpenClaw privacy guard that evaluates external data transmissions and decides whether to send, anonymize, cancel, or block them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreqingyuwu](https://clawhub.ai/user/andreqingyuwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to add a passive privacy review before an agent sends user data to external destinations such as APIs, email, uploads, posts, webhooks, or clipboard actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The instruction-only guard may allow passwords, medical data, or local secrets to be sent externally with too little protection. <br>
Mitigation: Review carefully before installing; tighten the policy to forbid plaintext credential sharing, narrowly scope local secret access, and require explicit verification for sensitive external disclosures. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Natural-language decision guidance and brief user notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in full transmission, anonymized transmission, cancellation, or phishing block.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
