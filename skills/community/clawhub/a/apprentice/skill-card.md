## Description: <br>
Apprentice lets an agent learn a repeatable local workflow by observing a user-described task once, then saving it as an editable workflow that can be replayed later. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Taha2053](https://clawhub.ai/user/Taha2053) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Apprentice to teach recurring command-line or narrated workflows once, review the generated workflow, and replay or refine it later from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learned workflows and observation logs may permanently store narrated procedures, sensitive project details, or credentials if the user teaches them. <br>
Mitigation: Do not teach secrets, API keys, deployment credentials, or account-changing routines; review and edit saved SKILL.md and observation.json files before reuse or sharing. <br>
Risk: Generated workflow scripts can run local bash commands with the user's authority. <br>
Mitigation: Preview or dry-run workflows first, review generated run.sh files before execution, and use separate sandboxing for destructive or high-impact routines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Taha2053/apprentice) <br>
- [Project Homepage](https://github.com/Taha2053/apprentice) <br>
- [README](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated local workflow files, JSON observation logs, and bash run scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflows are stored locally under apprentice/workflows/ and may include SKILL.md, observation.json, run.sh, and run_log.json files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
