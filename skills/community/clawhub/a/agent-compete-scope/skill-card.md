## Description: <br>
Analyzes competitor positioning, builds comparison matrices, and identifies whitespace strategy opportunities for a user's product. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinu4you](https://clawhub.ai/user/jinu4you) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Product marketers, founders, and strategy teams use this agent to compare a product against named competitors, summarize competitor profiles, and identify whitespace opportunities with recommended positioning moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Competitor-research inputs and generated analysis are sent to Tavily and the selected external LLM provider. <br>
Mitigation: Avoid confidential strategy or customer data unless those providers are approved for the intended use. <br>
Risk: API keys are required for web search and LLM calls. <br>
Mitigation: Use dedicated, limited-scope API keys and rotate them according to the organization's credential policy. <br>
Risk: The default npm start path runs mock job behavior that may not match production orchestration. <br>
Mitigation: Review or disable the mock behavior before production use. <br>


## Reference(s): <br>
- [Agent Compete Scope on ClawHub](https://clawhub.ai/jinu4you/agent-compete-scope) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [JSON response containing competitor profiles, comparison matrix rows, whitespace findings, and a markdown strategy recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires competitor names and a product description; optional focus values are pricing, features, positioning, or all.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
