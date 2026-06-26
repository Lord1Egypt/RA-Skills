## Description: <br>
Axioma Safe Cron Creator helps an agent create, verify, replace, and remove persistent user crontab entries for Python scripts while avoiding OpenClaw agent-session collisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to schedule Python scripts through user crontab, inspect scheduled jobs, and remove or replace existing cron entries. It is most relevant when direct system scheduling is preferred over OpenClaw agent-session execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent durable scheduling authority by creating or changing persistent user crontab entries. <br>
Mitigation: Review the exact crontab entry, target script, schedule, log path, and removal path before execution. <br>
Risk: The isolation claim is limited and does not prove that scheduled scripts are otherwise sandboxed or safe. <br>
Mitigation: Treat isolation as avoiding OpenClaw agent-session files only, and inspect target scripts and helper scripts separately before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axioma-safe-cron-creator) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated wrapper code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent crontab changes, wrapper scripts, log paths, and verification commands.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
