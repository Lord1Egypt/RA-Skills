## Description: <br>
Publishes plain-text posts and generated daily Web3, AI, and macro news briefings to Binance Square using a user-provided Square OpenAPI key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RenYuKe-CN](https://clawhub.ai/user/RenYuKe-CN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and social media operators use this skill to prepare and publish Binance Square text posts, token-tagged commentary, and daily news briefings. It is intended for workflows where the user supplies their own Square OpenAPI key and reviews the final content before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Binance Square API key with public posting authority. <br>
Mitigation: Store the key as a secret, use only a key you are comfortable granting posting authority to, and avoid exposing the full key in prompts or logs. <br>
Risk: Generated or scheduled posts may publish public content before the user has reviewed it. <br>
Mitigation: Require the agent to show the exact final post and wait for explicit user confirmation before publishing to Binance Square. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RenYuKe-CN/binance-square-publish) <br>
- [Binance Square OpenAPI](https://www.binance.com/zh-CN/square/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command examples; successful posting returns a Binance Square post URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports plain-text posts with token and topic tags; artifact guidance recommends keeping content under 2000 characters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
