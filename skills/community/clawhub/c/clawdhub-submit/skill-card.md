## Description: <br>
Guides users through ClawdHub skill submission, troubleshooting publishing failures, checking required files, and choosing web, CLI, or GitHub import workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahongting](https://clawhub.ai/user/mahongting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to diagnose failed ClawdHub submissions, verify skill packaging requirements, and follow an appropriate publishing path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested CLI commands may be run in the wrong directory or against the wrong skill. <br>
Mitigation: Confirm the target skill path, slug, and account before running publish or troubleshooting commands. <br>
Risk: Login tokens or publishing credentials could be exposed while following CLI examples. <br>
Mitigation: Keep tokens private, verify the ClawdHub CLI package/source before installation, and avoid sharing command history containing credentials. <br>
Risk: Publishing guidance may become stale as ClawdHub workflows or API behavior change. <br>
Mitigation: Check the current ClawdHub web flow and official documentation before relying on a workaround. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mahongting/clawdhub-submit) <br>
- [ClawdHub documentation](https://docs.openclaw.ai/zh-CN/tools/clawhub) <br>
- [Clawdhub repository link from artifact metadata](https://github.com/mahongting/clawdhub-submit-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No bundled executable code; users decide whether to run suggested commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
