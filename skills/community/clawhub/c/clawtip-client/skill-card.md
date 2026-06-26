## Description: <br>
AI离谱甲方 turns a normal design, copywriting, or programming brief into intentionally unreasonable client feedback, an inner monologue, and a final outcome after payment verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hepeihui](https://clawhub.ai/user/hepeihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this paid entertainment skill to generate satirical client feedback for design, copywriting, or programming briefs. The agent creates an order, passes payment flow details to the companion payment skill, then returns the generated client-feedback experience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The paid flow can report success without verified payment. <br>
Mitigation: Confirm the payment amount and recipient independently and prefer a version that fails closed on payment errors. <br>
Risk: Briefs and order data may include sensitive client or business details. <br>
Mitigation: Avoid entering sensitive information and delete or protect completed order files after use. <br>
Risk: The skill depends on a localhost service for order creation and result retrieval. <br>
Mitigation: Install only when the required local service is understood and documented for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hepeihui/clawtip-client) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hepeihui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown-style text with command examples and order status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an order number and stored payment credential for the final generation step; may use a local fallback response if the result service is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
