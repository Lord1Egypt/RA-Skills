## Description: <br>
Payment requests and delivery for AI agents and humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirch](https://clawhub.ai/user/kirch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use Clawpay to create crypto payment requests, share payment links, check payment status, and optionally deliver results after payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may send crypto payments to the wrong recipient, for the wrong amount, or with unintended delivery payloads. <br>
Mitigation: Verify the recipient wallet address, amount, currency, request ID, pay URL, and delivery payload before paying or delivering, and avoid sending sensitive deliverables unless they are intended to leave the local agent context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirch/clawpay) <br>
- [Clawpay homepage](https://clawpay.ai) <br>
- [Clawpay API base](https://clawpay.ai/v1) <br>
- [Clawpay skill file](https://clawpay.ai/skill.md) <br>
- [Clawpay heartbeat file](https://clawpay.ai/heartbeat.md) <br>
- [Clawpay metadata file](https://clawpay.ai/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with shell command snippets and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment request IDs, pay URLs, payment status checks, and optional delivery payload instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
