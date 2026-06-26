## Description: <br>
Deprecated legacy connector skill. Use @launchthatbot/connect-openclaw-plugin for all new LaunchThatBot OpenClaw connect flows with configurable permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[launchthatbot](https://clawhub.ai/user/launchthatbot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw operators use this skill to connect existing OpenClaw infrastructure to LaunchThatBot for heartbeat, event ingest, replay checks, and live visibility while migrations to the replacement plugin are completed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This is a deprecated legacy connector; using it for new setups may miss the replacement plugin's configurable permissions. <br>
Mitigation: Use @launchthatbot/connect-openclaw-plugin for new connections and reserve this connector for existing deployments that intentionally need it. <br>
Risk: The connector sends scoped OpenClaw status and event data, including optional metadata, to a configured LaunchThatBot endpoint. <br>
Mitigation: Verify the base URL, avoid sensitive values in event metadata, and restrict egress to the expected LaunchThatBot domain. <br>
Risk: Ingest tokens and optional signing secrets are required for authenticated operation. <br>
Mitigation: Provide secrets through environment injection, a secret manager, or secure files; keep them out of CLI history, logs, and screenshots. <br>
Risk: The local retry queue can persist event data on disk. <br>
Mitigation: Use restrictive queue-file permissions and disable queue persistence with --persist-queue=false when local event storage is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Connector listing](https://clawhub.ai/launchthatbot/connector) <br>
- [LaunchThatBot connect documentation](https://launchthatbot.com/docs/skills/connect) <br>
- [LaunchThatBot import documentation](https://launchthatbot.com/docs/skills/import) <br>
- [README](artifact/README.md) <br>
- [Security policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides connector setup, hardening, troubleshooting guidance, and CLI commands; the auth-link command can emit JSON.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
