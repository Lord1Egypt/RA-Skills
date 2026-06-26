## Description: <br>
Supports sending order inquiries for specified 1688 orders, including single-order inquiries and parallel batch inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to ask merchants questions about 1688 supply-chain orders, including delivery timing, availability, refunds, images, and target-price negotiation. It can split multiple orders into separate inquiry tasks when each order needs a different question or target total price. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a 1688 account access key. <br>
Mitigation: Install only when the publisher is trusted, and prefer environment or platform secret injection over plaintext local configuration. <br>
Risk: The skill can send order IDs, questions, optional images, and merchant-facing inquiries to 1688 gateway services. <br>
Mitigation: Ask for explicit user confirmation before sending inquiries, with extra care for batch inquiries. <br>
Risk: The skill reports usage metadata with limited user controls. <br>
Mitigation: Review the usage-reporting behavior before deployment and ensure it matches the deployment's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-supplychain-order-inquiry) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [inquiry_send capability](artifact/references/capabilities/inquiry_send.md) <br>
- [batch_inquiry capability](artifact/references/capabilities/batch_inquiry.md) <br>
- [configure capability](artifact/references/capabilities/configure.md) <br>
- [Common error handling](artifact/references/common/error-handling.md) <br>
- [Skill usage reporting notes](artifact/references/skill埋点说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [JSON containing a success flag, user-facing markdown, and structured data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are run through a Python CLI and may send order IDs, questions, optional images, and usage metadata to 1688 gateway services.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
