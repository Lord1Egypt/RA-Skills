## Description: <br>
Gateway Manager Free helps agents produce declarative API gateway routes, authentication, rate limits, monitoring snippets, and configuration guidance for Kong, APISIX, Nginx, and Envoy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and operations teams use this skill to ask an agent for API gateway configuration, route normalization, authentication patterns, rate-limit settings, monitoring snippets, and gateway selection guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Activation metadata includes unrelated project-management language while the skill requests write and command-execution capability. <br>
Mitigation: Narrow activation metadata to API gateway tasks and require explicit user direction before writing files or running commands. <br>
Risk: Generated gateway, authentication, and rate-limit configurations may be unsafe or incorrect if deployed without review. <br>
Mitigation: Validate generated configuration in a test environment, review route precedence and authentication behavior, and keep secrets in environment variables or a managed secret store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/gateway-manager-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML, JSON, shell, and gateway configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployable gateway configuration examples and commands that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
