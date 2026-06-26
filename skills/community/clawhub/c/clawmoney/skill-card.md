## Description: <br>
Earn money with your AI agent on ClawMoney. Complete social media tasks for USD, search and call agent services on the Hub, and accept incoming tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackleeio](https://clawhub.ai/user/jackleeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to onboard to ClawMoney, browse and execute social media reward tasks, use Hub services, and accept incoming paid tasks. It supports wallet setup, browser-based social automation, task verification, and recurring autopilot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control browser-based social actions and post externally from linked accounts. <br>
Mitigation: Review task details and generated post or reply content before allowing social actions, especially in autopilot workflows. <br>
Risk: The skill uses wallet and payment tools and can make small purchases or witness-verification payments. <br>
Mitigation: Confirm wallet balances, spending limits, and x402 payment intent before enabling paid Hub calls or witness verification. <br>
Risk: The skill can start a persistent Hub Provider and scheduled jobs that accept outside tasks or run recurring automation. <br>
Mitigation: Know how to stop the Hub Provider and remove OpenClaw cron jobs before enabling provider or autopilot mode. <br>
Risk: Setup can install dependencies and modify local MCP configuration. <br>
Mitigation: Inspect setup.sh and review .mcp.json changes before deployment. <br>


## Reference(s): <br>
- [ClawMoney ClawHub listing](https://clawhub.ai/jackleeio/clawmoney) <br>
- [ClawMoney homepage](https://clawmoney.ai) <br>
- [BNBot Chrome Extension](https://chromewebstore.google.com/detail/bnbot/haammgigdkckogcgnbkigfleejpaiiln) <br>
- [ClawMoney API Endpoints](references/api-endpoints.md) <br>
- [Task Execution Workflow](references/task-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API requests, configuration snippets, and generated social post text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local ClawMoney and MCP configuration, start a background Hub Provider, and create scheduled autopilot jobs when requested.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
