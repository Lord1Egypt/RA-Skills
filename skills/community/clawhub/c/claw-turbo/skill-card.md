## Description: <br>
Zero-latency regex-based skill routing middleware for OpenClaw that intercepts known user commands with compiled patterns and executes matching skill scripts directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacobye2017-afk](https://clawhub.ai/user/jacobye2017-afk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation operators use this skill to route repeated OpenClaw commands through regex-matched actions while forwarding unmatched requests to the local LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Matched routes can turn ordinary messages into immediate local shell actions such as deploys, service restarts, refunds, printing, or account-changing operations. <br>
Mitigation: Use narrow explicit routes, run the proxy as a least-privileged user, and require confirmation, authorization, input validation, audit logs, and rollback controls for high-impact actions. <br>
Risk: The release security verdict is suspicious because the artifact documents fast command execution without documented safety gates. <br>
Mitigation: Review and pin the external GitHub source before installing, start with low-risk routes, and avoid production use until the configured actions have been tested and approved. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jacobye2017-afk/claw-turbo) <br>
- [Project homepage](https://github.com/jacobye2017-afk/claw-turbo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes may execute local shell commands immediately when configured patterns match user messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
