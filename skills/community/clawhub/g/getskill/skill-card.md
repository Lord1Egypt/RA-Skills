## Description: <br>
GetSkill helps OpenClaw users search, install, update, list, and configure skills through the @workskills/getskill CLI and getskill.work skill repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlei9](https://clawhub.ai/user/zlei9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use GetSkill to discover skills, install them into a local OpenClaw skills directory, update cached skill repositories, list installed skills, and configure API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install and update workflows copy remote skill repository contents into the local OpenClaw skills directory, where copied skills can persist and affect agent behavior. <br>
Mitigation: Install or update only from trusted publishers and repositories, and review or scan target skill source before deployment. <br>
Risk: Custom API endpoints can direct the CLI to untrusted repositories or altered skill listings. <br>
Mitigation: Use custom API endpoints only when the endpoint and the repositories it returns are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlei9/getskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands and expected behavior for search, install, update, list, path, config, and clean workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
