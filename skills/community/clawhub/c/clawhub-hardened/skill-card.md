## Description: <br>
Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com, including fetching new skills, syncing installed skills, and publishing skill folders with the npm-installed CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate ClawHub CLI workflows for discovering, installing, updating, listing, authenticating, and publishing agent skills while applying safety guardrails around global installs, bulk updates, and output handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide package-management operations that install, update, or publish agent skills. <br>
Mitigation: Install only trusted ClawHub CLI packages and registries, prefer targeted or interactive updates, and use fresh confirmation for destructive or bulk operations. <br>
Risk: Forced non-interactive updates can silently replace local skills and bypass review prompts. <br>
Mitigation: Avoid combining --force with --no-input for bulk updates unless the user gives explicit current-turn confirmation after the risks are explained. <br>
Risk: ClawHub CLI output may expose local paths, installed skill names, or authentication identity. <br>
Mitigation: Do not pipe ClawHub CLI output to public network services, webhooks, paste sites, or HTTP endpoints; display it locally instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/clawhub-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [ClawHub registry](https://clawhub.com) <br>
- [Faberlens ClawHub safety evaluation](https://faberlens.ai/explore/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the npm-installed clawhub CLI for command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
