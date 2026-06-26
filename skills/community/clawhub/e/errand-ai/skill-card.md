## Description: <br>
Post errands using natural language, track status, review submissions, and automate USDC payments through the ErrandAI task marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users can use this skill to create, track, and review paid errands for human workers through ErrandAI. It supports tasks such as photography, product verification, price research, translation, research, delivery, and general custom errands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create paid errands and approve submissions that release USDC without a clear confirmation guardrail. <br>
Mitigation: Require manual confirmation outside the skill before posting paid errands or approving submissions, and avoid auto-approval or scheduled paid workflows unless spending limits and audit controls are in place. <br>
Risk: A misconfigured ErrandAI API endpoint could send credentials or payment-related actions to an unintended service. <br>
Mitigation: Keep ERRANDAI_API_URL pointed at the official ErrandAI service and use a scoped or revocable API key where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChloePark85/errand-ai) <br>
- [ErrandAI documentation](https://docs.errand.be) <br>
- [ErrandAI dashboard](https://errand.be/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown-formatted status, confirmation, error, and review messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger ErrandAI API actions that create paid errands or approve submitted work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
