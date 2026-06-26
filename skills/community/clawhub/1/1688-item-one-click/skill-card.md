## Description: <br>
1688 Item One Click lets an agent check and, after user confirmation, update 1688 item titles, main images, limited-time discounts, and member posts through signed CLI calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External commerce operators and their agents use this skill to apply approved changes to 1688 listings and member posts after a pre-check and explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured 1688 AccessKey can authorize merchant write operations, including listing changes, member posts, and potential discounts. <br>
Mitigation: Use the narrowest available key scope, store it only in the intended OpenClaw configuration path, and rotate it if exposure is suspected. <br>
Risk: The execute command can directly modify product data or pricing-related settings. <br>
Mitigation: Run before_check first, present the proposed item ID, spi_code, and parameters to the user, and call execute only after explicit confirmation. <br>
Risk: Incorrect item IDs, image URLs, discount values, or member-post content could publish unintended merchant changes. <br>
Mitigation: Validate each item ID and parameter against the user's request before approval, especially discountRate and activityDay values. <br>
Risk: A misdirected gateway URL could send credentials or signed requests to an unintended service. <br>
Mitigation: Keep OPENCLAW_GATEWAY_URL trusted and local unless the deployment explicitly requires a different trusted endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-item-one-click) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Pre-check capability guide](artifact/capabilities/before_check.md) <br>
- [Execution capability guide](artifact/capabilities/execute.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output with human-facing Markdown status messages and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and a configured 1688 AccessKey before authenticated operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
