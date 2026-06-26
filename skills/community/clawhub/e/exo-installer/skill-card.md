## Description: <br>
Install, update, and monitor E.x.O. tools such as jasper-recall, hopeIDS, context compaction, OpenClaw plugins, and health checks from one installer workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emberDesire](https://clawhub.ai/user/emberDesire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to install E.x.O. command-line tools and plugins, check their health, apply updates, and prepare optional OpenClaw cron monitoring. It is most useful when managing several E.x.O. ecosystem packages from one agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to install or update npm packages and run package setup commands. <br>
Mitigation: Ask for explicit user approval before running `exo install --all`, installing individual packages, or running `exo update`; install only trusted E.x.O. packages. <br>
Risk: Internal clone operations require GitHub access and may fetch private repositories and install their dependencies. <br>
Mitigation: Confirm repository access and intent before running `exo internal clone`, then review the cloned projects and dependency install behavior before use. <br>
Risk: Cron setup can add recurring OpenClaw health-check behavior with optional Telegram reporting. <br>
Mitigation: Review the generated cron payload and notification behavior before adding it to OpenClaw cron. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emberDesire/exo-installer) <br>
- [npm package](https://www.npmjs.com/package/exo-installer) <br>
- [E.x.O. product documentation](https://exohaven.com/products) <br>
- [GitHub repository link disclosed in artifact](https://github.com/E-x-O-Entertainment-Studios-Inc/exo-installer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON health-check output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose global npm installs, package updates, GitHub clone commands, OpenClaw cron configuration, and health-check summaries.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
