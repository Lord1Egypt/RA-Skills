## Description: <br>
AP2 Agent-to-Agent mock checkout (SuperShoe). HP/HNP with card or x402 via mcporter and local mock MCP. No real payments. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[xielianghai](https://clawhub.ai/user/xielianghai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to exercise a local AP2 checkout scenario for SuperShoe purchases, including human-present and human-not-present flows with card or x402 payment rails. It is intended for simulated local checkout behavior, not real payment settlement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-command npx installer is outside this skill package and is documented to patch OpenClaw and start local backend services. <br>
Mitigation: Review the AP2 repository installer before running it, or use the manual setup path with an explicit AP2_HOME and the bundled backend check script. <br>
Risk: The skill drives local AP2 mock MCP services and requires localhost ports 8091-8094 and 8100-8103. <br>
Mitigation: Run it only in an intended local demo environment and verify the backend ports before starting a checkout flow. <br>
Risk: Checkout steps can resemble payment actions even though settlement is simulated. <br>
Mitigation: Show the item, price cap, and payment rail before mandate signing, and proceed only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xielianghai/ap2-checkout) <br>
- [Setup reference](references/setup.md) <br>
- [mcporter schema](https://raw.githubusercontent.com/steipete/mcporter/main/mcporter.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces simulated checkout flow instructions and a final purchase_complete JSON object.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
