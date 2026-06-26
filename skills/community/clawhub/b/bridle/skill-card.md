## Description: <br>
Unified configuration manager for AI coding assistants. Manage profiles, install skills/agents/commands, and switch configurations across Claude Code, OpenCode, Goose, and Amp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjesuiter](https://clawhub.ai/user/bjesuiter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Bridle to manage AI coding assistant profiles, install skills, agents, commands, and MCPs, and switch configurations across Claude Code, OpenCode, Goose, and Amp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bridle can modify existing assistant configuration and install assistant components. <br>
Mitigation: Install and run it only when configuration changes are intended, and review affected profiles and component contents before applying changes. <br>
Risk: Installing components from external GitHub repositories can introduce supply-chain risk. <br>
Mitigation: Use the GitHub install feature only with repositories you trust and inspect component contents before installation. <br>
Risk: Force overwrite and delete or uninstall operations can change or remove existing assistant setups. <br>
Mitigation: Use force overwrite, delete, and uninstall commands carefully, preferably after checking current status and preserving needed configuration. <br>


## Reference(s): <br>
- [ClawHub Bridle listing](https://clawhub.ai/bjesuiter/bridle) <br>
- [Publisher profile: bjesuiter](https://clawhub.ai/user/bjesuiter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may emit human-readable text, JSON, or automatic TTY-dependent output when run through the Bridle CLI.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
