## Description:

Managed mining over public game APIs using X-Api-Code authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhzai30](https://clawhub.ai/user/zhzai30)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to manage OpenClaw mining sessions, check mining and stamina state, collect incremental session events, and start or stop automated mining loops through documented tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved game API codes can be exposed through the local service or persisted cache.

Mitigation: Run the service only on a trusted local machine or behind strong authentication, avoid shared cache keys such as default, clear cached codes when finished, and rotate any apiCode that may have been stored or exposed.

Risk: Mining automation and stamina purchase tools can spend account resources, including diamonds when auto-buy is enabled.

Mitigation: Keep auto-buy disabled unless automatic diamond spending is intended, set conservative failure limits, and monitor stamina and diamond status before starting long-running loops.

Risk: The server security verdict is suspicious because the local HTTP service is under-protected for secret storage and resource-spending actions.

Mitigation: Review before installing, restrict network exposure, and treat the apiCode as an account secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhzai30/skills/clawquest-agent-mine-openclaw)
- [ClawHub publisher profile](https://clawhub.ai/user/zhzai30)
- [Configured game API base URL](https://api.km.cocweb3.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tool names, JSON-style API responses, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can expose session status, cached API-code state, mining events, stamina data, and upstream game API responses.]

## Skill Version(s):

1.0.11 (source: server release evidence; artifact frontmatter reports 1.0.10 and package.json reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
