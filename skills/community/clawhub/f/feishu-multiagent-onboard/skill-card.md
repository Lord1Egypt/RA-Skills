## Description:

Provides an interactive wizard to configure and validate multiple OpenClaw agents for Feishu channels with diagnostic tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoopools](https://clawhub.ai/user/zoopools)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to configure Feishu channel accounts, bind multiple agents to Feishu apps, validate the configuration, and troubleshoot common setup issues before gateway restart and pairing approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects Feishu App Secrets and stores them in the persistent OpenClaw configuration.

Mitigation: Protect the configuration file, avoid use on shared machines, and rotate Feishu App Secrets if they are exposed.

Risk: The wizard can replace or broaden Feishu account and binding settings in the persistent OpenClaw configuration.

Mitigation: Back up ~/.openclaw/openclaw.json first, review existing bindings, and inspect the saved configuration before restarting the gateway or approving pairings.

Risk: Diagnostic mode reads local OpenClaw status and logs that may expose operational details.

Mitigation: Review diagnostic output before sharing it and redact secrets, account IDs, pairing codes, and environment-specific paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoopools/skills/feishu-multiagent-onboard)
- [Configuration guide](artifact/docs/guide.md)
- [FAQ](artifact/docs/faq.md)
- [Feishu Open Platform app console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with configuration edits and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Feishu account and binding configuration to the user's persistent OpenClaw configuration file.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact clawhub.json, and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
