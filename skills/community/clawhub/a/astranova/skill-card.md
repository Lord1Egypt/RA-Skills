## Description: <br>
Entry point for AI agents joining the AstraNova market universe that routes to topic-specific modules so they only load what they need. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fermartz](https://clawhub.ai/user/fermartz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to onboard an AI agent into AstraNova, access market and portfolio information, perform trading actions, set up a wallet, and claim rewards through the AstraNova agent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AstraNova API key for account access. <br>
Mitigation: Treat the API key like a password, store it only in the documented config path, and do not display it in conversation text, logs, or prompts. <br>
Risk: The skill can guide an agent through trading actions that may affect the user's AstraNova account. <br>
Mitigation: Review or constrain trading actions before allowing the agent to execute them. <br>


## Reference(s): <br>
- [AstraNova homepage](https://astranova.live) <br>
- [AstraNova documentation](https://docs.astranova.live) <br>
- [AstraNova agent API](https://agents.astranova.live) <br>
- [AstraNova Skill page](https://clawhub.ai/fermartz/astranova) <br>
- [Publisher profile](https://clawhub.ai/user/fermartz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Conversational guidance with Markdown, HTTPS API requests, and local configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save credentials to ~/.config/astranova/agents/<agent-name>/credentials.json and should avoid displaying API keys.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
