## Description: <br>
Call Fetch.ai Agentverse agents by address. Search the Agentverse marketplace, browse a curated catalog of top agents (Tavily Search, ASI1-Mini, DALL-E 3, Technical Analysis, Asset Signal, Translator, Statistics, Github), and send ChatMessages to any agent. Use when working with Fetch.ai, Agentverse, uAgents, decentralized AI agents, or when the user wants to discover or message an agent on the Fetch.ai network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steve-dusty](https://clawhub.ai/user/steve-dusty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover Fetch.ai Agentverse agents, inspect a curated agent catalog, and send user prompts to selected agents for search, translation, statistics, image generation, GitHub metadata, and market-signal style responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Agentverse API key. <br>
Mitigation: Use a scoped key where possible, keep it out of prompts and logs, and rotate it if the environment is shared or exposed. <br>
Risk: User prompts are forwarded to Fetch.ai Agentverse agents and may include sensitive context. <br>
Mitigation: Avoid sending secrets, private business data, or regulated personal data unless the destination agent and data handling are approved. <br>
Risk: The skill creates reusable local agent state and stores the latest result in a predictable temporary file. <br>
Mitigation: Run it in an isolated workspace for sensitive use, review local state handling, and clear temporary response files after use. <br>
Risk: Third-party agent responses, including market or crypto-related outputs, can be incorrect or misleading. <br>
Mitigation: Verify outputs against authoritative sources before acting on them, especially for financial, operational, or security-sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steve-dusty/fetch-agents) <br>
- [Mailbox setup](references/mailbox-setup.md) <br>
- [Agentverse agent search endpoint](https://agentverse.ai/v1/search/agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Natural-language replies and formatted lists, with JSON from catalog and marketplace search helpers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent calls may take 30-60 seconds and depend on Agentverse agent availability, mailbox setup, Python, uagents packages, and AGENTVERSE_API_KEY.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
