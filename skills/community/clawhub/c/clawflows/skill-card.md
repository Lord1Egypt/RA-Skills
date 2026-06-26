## Description: <br>
Search, install, and run multi-skill automations from clawflows.com that combine skills through workflow logic, conditions, and data flow between steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cluka-399](https://clawhub.ai/user/Cluka-399) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation builders use this skill to discover, install, check, run, schedule, inspect, and publish ClawFlows automations that coordinate multiple capability-providing skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded or registry-provided workflows can chain installed skills and produce real side effects. <br>
Mitigation: Review the npm package and workflow YAML before use, run `clawflows check`, and start with `--dry-run`. <br>
Risk: Automations may affect external systems such as email, calendars, databases, publishing tools, or cron schedules. <br>
Mitigation: Avoid untrusted registry workflows and require additional review before enabling workflows that write to external services or scheduled jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cluka-399/clawflows) <br>
- [ClawFlows registry](https://clawflows.com) <br>
- [ClawFlows CLI on npm](https://www.npmjs.com/package/clawflows) <br>
- [ClawFlows registry GitHub repository](https://github.com/Cluka-399/clawflows-registry) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to install and run the clawflows CLI; dry-run and review steps are recommended before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
