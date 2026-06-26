## Description: <br>
OpenClaw plugin that scrubs private infrastructure details from outgoing messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to reduce accidental disclosure of private infrastructure details in outgoing messages before delivery to chat surfaces such as Discord, Telegram, and Signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security evidence marks the artifact review suspicious because the workspace did not expose a coherent single skill artifact to verify. <br>
Mitigation: Confirm the installed package contains the intended SKILL.md, index.ts, openclaw.plugin.json, and package.json files, then rerun review on the exact artifact before deployment. <br>
Risk: Allowed recipients bypass scrubbing and dry-run mode logs matches without redacting message content. <br>
Mitigation: Keep allowedRecipients narrowly scoped, verify dryRun is false for normal use, and test redaction behavior before enabling the plugin on production messaging channels. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/solomonneas/content-scrubber) <br>
- [Publisher profile](https://clawhub.ai/user/solomonneas) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Redacted message text and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic regex-based message interception with dry-run and allowed-recipient configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
