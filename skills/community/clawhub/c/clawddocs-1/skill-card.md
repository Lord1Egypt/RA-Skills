## Description: <br>
Clawdbot documentation expert with decision tree navigation, search scripts, doc fetching, version tracking, and config snippets for all Clawdbot features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to navigate Clawdbot documentation, find relevant setup and troubleshooting pages, and produce configuration guidance for Clawdbot providers, gateway settings, automation, tools, platforms, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release metadata and artifact metadata disagree on version and license, which can make publisher review or dependency tracking ambiguous. <br>
Mitigation: Use the server-resolved release metadata for this card, and verify the publisher, release version, and license before deployment. <br>
Risk: Configuration examples involve bot tokens and session paths, which could expose credentials if users paste real secrets into prompts. <br>
Mitigation: Keep real bot tokens and session data in environment variables or a secret manager, and use placeholders in agent-visible examples. <br>
Risk: Included shell scripts are documentation helpers and may change in future releases. <br>
Mitigation: Review script contents after updates before running them in a production workspace. <br>


## Reference(s): <br>
- [Clawddocs 1 ClawHub page](https://clawhub.ai/tigertamvip/clawddocs-1) <br>
- [Clawdbot documentation](https://docs.clawd.bot/) <br>
- [Clawdbot Discord provider documentation](https://docs.clawd.bot/providers/discord) <br>
- [Common configuration snippets](snippets/common-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite Clawdbot documentation pages and provide configuration snippets using environment-variable placeholders for secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
