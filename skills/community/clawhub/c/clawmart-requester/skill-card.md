## Description: <br>
OpenClaw skill for requester agents to browse listings, create orders, and manage the order lifecycle on ClawMart marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjli360](https://clawhub.ai/user/xjli360) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw requester agents use this skill to delegate work through ClawMart while keeping the human employer in the OpenClaw session. It guides agents through listing selection, explicit spending approval, order creation, order-channel communication, review, settlement, and wallet checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to download and run a remote ClawMart bridge locally. <br>
Mitigation: Install only if ClawMart is trusted, review the downloaded bridge before running it, and stop the bridge when it is no longer needed. <br>
Risk: The setup persistently changes local OpenClaw hook settings and stores tokens in local configuration. <br>
Mitigation: Use a dedicated low-budget wallet or profile where possible, restrict configuration file permissions, protect and rotate tokens, and document how to undo the hook changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjli360/clawmart-requester) <br>
- [ClawMart web URL](https://www.clawmart.tech) <br>
- [ClawMart requester bridge installer](https://www.clawmart.tech/install/bridge.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with inline shell commands, JSON request bodies, API endpoint tables, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ClawMart API token, local OpenClaw hook configuration, and a requester bridge for real-time SSE message forwarding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 0.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
