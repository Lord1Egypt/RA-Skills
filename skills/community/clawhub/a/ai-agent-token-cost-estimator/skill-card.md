## Description: <br>
Estimate token usage and approximate API cost of AI agents by analyzing model choice, reasoning steps, tool use, and expected output size before deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShowMeTheMoney2023](https://clawhub.ai/user/ShowMeTheMoney2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI builders and developers use this skill to estimate per-run token consumption and API cost for an agent workflow before running it in production. It helps identify cost drivers such as model size, reasoning steps, tool calls, context growth, and long outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost estimates can be inaccurate if model prices, prompt sizes, tool retries, or runtime behavior differ from the user's assumptions. <br>
Mitigation: Validate estimates against current provider pricing and production telemetry, and use token, step, retry, and budget limits for deployed agents. <br>
Risk: Users may include confidential prompts or proprietary workflow details when requesting an estimate. <br>
Mitigation: Provide only the workflow details needed for cost estimation and omit sensitive prompts, credentials, customer data, or proprietary architecture. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ShowMeTheMoney2023/ai-agent-token-cost-estimator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style cost estimate with token range, cost range, primary cost drivers, and optimization suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Estimates are approximate and depend on the model pricing, prompt size, tool behavior, and runtime limits supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
