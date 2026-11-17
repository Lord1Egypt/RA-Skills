## Description: <br>
Api Toolkit Free helps agents draft and troubleshoot API requests by producing curl and HTTPie templates, authentication patterns, error-diagnosis guidance, and endpoint lookup notes for common third-party services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to generate API test requests, troubleshoot HTTP and API errors, and verify third-party service integrations before scripting or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl, OAuth, DELETE, POST, and ping commands can affect external services or local/network state if run without review. <br>
Mitigation: Review each command, endpoint, method, and payload before execution, and require explicit confirmation for mutating or destructive requests. <br>
Risk: API keys, tokens, and client secrets could be exposed if users paste real credentials into prompts, command text, or logs. <br>
Mitigation: Keep secrets in environment variables or secret stores, use placeholders in examples, and avoid echoing tokens or placing API keys in URLs unless the target service requires it. <br>
Risk: The skill has broad activation wording and may be mistaken for a general programming or deployment assistant. <br>
Mitigation: Use it for API request drafting, authentication examples, and troubleshooting guidance; rely on more specialized skills for general coding, production deployment, or infrastructure changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/api-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command blocks and tabular API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands use placeholder credentials; curl, OAuth, DELETE, POST, and ping commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
