## Description: <br>
Use this skill when the task should be done through the apitweet command-line client, including installing the CLI, configuring Twitter/X app or profile auth, previewing requests, and calling apitweet endpoints through convenience commands or raw paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliraza948](https://clawhub.ai/user/aliraza948) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, AI agent builders, growth teams, content operators, and automation workflows use this skill to run ApiTweet CLI commands for Twitter/X data retrieval, credential setup, dry-run previews, write actions, and Markdown-to-X-Article publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable credentialed Twitter/X automation, including write actions. <br>
Mitigation: Use --dry-run before write actions, verify the active profile or account, and execute only after the user clearly authorizes the action. <br>
Risk: Saved app and profile configuration can contain API keys, cookies, auth_token values, or ct0 values in plain JSON on disk. <br>
Mitigation: Avoid storing long-lived credentials on shared machines or CI runners and isolate APITWEET_CONFIG_DIR for testing or multi-user environments. <br>
Risk: Raw absolute URLs or untrusted endpoint paths may send saved credentials to unintended request targets. <br>
Mitigation: Use convenience commands where possible and avoid raw absolute URLs or untrusted endpoint paths when credentials are configured. <br>
Risk: The auth cookie workflow places an auth_token in a request path. <br>
Mitigation: Treat logs, traces, and network boundaries as sensitive when using auth cookie commands. <br>


## Reference(s): <br>
- [ApiTweet](https://apitweet.com) <br>
- [ApiTweet dashboard](https://apitweet.com/dashboard) <br>
- [ClawHub skill page](https://clawhub.ai/aliraza948/apitweet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to prefer dry-run previews before write actions and to avoid echoing raw credentials.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence; package.json in artifact reports 0.1.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
