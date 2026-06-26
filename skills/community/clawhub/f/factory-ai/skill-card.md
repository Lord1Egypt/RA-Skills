## Description: <br>
Use Factory AI's droid CLI to interactively build, debug, refactor, review, and deploy code, with support for plugins, MCP servers, and multiple AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mitchellbernstein](https://clawhub.ai/user/mitchellbernstein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to invoke Factory AI's droid CLI for feature development, debugging, refactoring, code review, git operations, deployment, MCP server management, and plugin management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke a third-party coding agent CLI that modifies code, creates commits or PRs, deploys applications, installs plugins, and changes MCP servers. <br>
Mitigation: Require human review before applying code changes, commits, PRs, deployments, plugin installs, or MCP server changes. <br>
Risk: The `--force` option can auto-apply changes without confirmation. <br>
Mitigation: Avoid `droid exec --force` unless the operator explicitly intends unattended changes and has reviewed the requested action. <br>
Risk: The skill depends on trust in the installed Factory `droid` binary and authenticated account connection. <br>
Mitigation: Verify the binary source and version before use, and confirm account authorization and API key handling. <br>
Risk: Org-wide code context and session memory may persist beyond a single task. <br>
Mitigation: Confirm how Factory scopes, stores, and clears organization context and session memory before using the skill on sensitive code. <br>


## Reference(s): <br>
- [Factory AI Droid ClawHub page](https://clawhub.ai/mitchellbernstein/factory-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output when droid exec --json is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
