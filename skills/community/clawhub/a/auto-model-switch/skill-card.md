## Description: <br>
Automatically switches OpenClaw models when token limits or API rate limits would otherwise interrupt a conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wei-wei-zhao](https://clawhub.ai/user/wei-wei-zhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to monitor model token usage and rate-limit status, then switch to configured backup models manually or through heartbeat automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic switching can change the active OpenClaw model when heartbeat automation or gateway integration is enabled. <br>
Mitigation: Review config.yaml, confirm backup-model priority, and enable heartbeat automation only where automatic model changes are acceptable. <br>
Risk: Gateway integration uses OPENCLAW_GATEWAY_TOKEN when provided. <br>
Mitigation: Use a least-privilege gateway token where possible and keep the token out of shared logs, shell history, and committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wei-wei-zhao/auto-model-switch) <br>
- [README](README.md) <br>
- [Quickstart](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output with YAML configuration and JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local model-switch state and, when gateway credentials are configured, change the active OpenClaw model.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
