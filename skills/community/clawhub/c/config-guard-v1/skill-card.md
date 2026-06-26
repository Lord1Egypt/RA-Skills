## Description: <br>
Guides safer OpenClaw configuration edits with backup, redacted preview, JSON validation, and explicit user confirmation before changes are applied. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who maintain OpenClaw use this skill to inspect, validate, back up, and modify ~/.openclaw/openclaw.json for model, channel, tool, and skill settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security summary says the advertised redacted preview may expose API keys or tokens. <br>
Mitigation: Do not rely on preview redaction alone; inspect exact diffs locally, avoid sharing terminal previews, and redact secrets independently before display or logging. <br>
Risk: The skill is designed to edit OpenClaw configuration and may restart the gateway. <br>
Mitigation: Create an independent backup, validate JSON syntax, verify the intended diff, and confirm only after understanding any gateway restart impact. <br>


## Reference(s): <br>
- [OpenClaw configuration examples](references/examples.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Config Guard on ClawHub](https://clawhub.ai/justaboyhai-wq/config-guard-v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local OpenClaw configuration edits and preview output that should be treated as sensitive until independently verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
