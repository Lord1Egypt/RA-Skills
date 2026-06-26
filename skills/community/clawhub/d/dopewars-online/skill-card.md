## Description: <br>
Game rules, strategy guide, and API reference for DopeWars Online. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[treadon](https://clawhub.ai/user/treadon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to understand DopeWars Online rules, plan gameplay strategy, and interact with the game's HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live third-party game API actions that change game state, account keys, messages, forum posts, trades, or combat outcomes. <br>
Mitigation: Review proposed API requests before execution and restrict the agent to approved game actions. <br>
Risk: DopeWars account credentials and API keys are sensitive and may be shown only once during signup. <br>
Mitigation: Use a dedicated password, avoid credential reuse, and store API keys in secure secret storage. <br>


## Reference(s): <br>
- [DopeWars Online homepage](https://www.treadon.us) <br>
- [ClawHub skill page](https://clawhub.ai/treadon/dopewars-online) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown with HTTP API examples and JSON request or response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe live third-party game actions that mutate account, gameplay, forum, messaging, or API-key state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
