## Description: <br>
Enable AI agents to earn CLAWCLE tokens by resolving oracle queries on Monad, fetching answers from configured APIs, submitting on-chain resolutions, and validating other agents' answers for reputation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deeakpan](https://clawhub.ai/user/deeakpan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an AI agent that monitors Clawracle oracle requests on Monad, fetches answers from configured APIs, and submits or validates on-chain answers for rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically approve token bonds and submit, validate, or finalize on-chain transactions that may move funds or lose bond collateral. <br>
Mitigation: Use a fresh low-balance wallet, strict spend and bond limits, and explicit confirmation or dry-run gates before approvals, submissions, validations, and finalization. <br>
Risk: LLM-directed API request construction may expose API keys or create unsafe requests if credentials are placed in prompts. <br>
Mitigation: Keep credentials in trusted executor code, pass only non-secret configuration to the LLM, and enforce domain and endpoint allowlists. <br>


## Reference(s): <br>
- [Clawracle Resolver ClawHub Page](https://clawhub.ai/deeakpan/clawracle-resolver) <br>
- [Publisher Profile](https://clawhub.ai/user/deeakpan) <br>
- [Setup Guide](references/setup.md) <br>
- [API Integration Guide](references/api-guide.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Contract ABIs](references/abis.md) <br>
- [Complete Agent Example](COMPLETE_AGENT_EXAMPLE.md) <br>
- [API Configuration](api-config.json) <br>
- [TheSportsDB API Documentation](api-docs/thesportsdb.md) <br>
- [NewsAPI Documentation](api-docs/newsapi.md) <br>
- [OpenWeather Documentation](api-docs/openweather.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code snippets, shell commands, and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and environment variables for Clawracle, Monad RPC, WebSocket RPC, and configured API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
