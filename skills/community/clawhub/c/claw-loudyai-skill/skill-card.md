## Description: <br>
Automates Loudy.ai task workflows by listing earning pools, submitting user-provided task links, and checking review and payment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfsf332](https://clawhub.ai/user/sfsf332) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to manage Loudy.ai earning-pool tasks from an agent session, including reviewing available pools, submitting manually created X/Twitter post links, and checking audit or payment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LOUDY_API_KEY exposure could allow unauthorized Loudy.ai API access. <br>
Mitigation: Keep LOUDY_API_KEY in an environment variable and do not store it in shared files. <br>
Risk: The installer can clone files and replace an existing installation directory. <br>
Mitigation: Prefer installing from the reviewed package instead of running the curl-to-bash installer, and do not run install.sh where local changes may be overwritten. <br>
Risk: Optional cron polling creates ongoing background checks and workspace status files. <br>
Mitigation: Enable cron only when continuous polling is intended, and review the configured workspace path before activation. <br>
Risk: The skill may recommend a separate Binance or X posting skill for some tasks. <br>
Mitigation: Vet any separate posting skill independently before installation or use. <br>


## Reference(s): <br>
- [Loudy.ai API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sfsf332/claw-loudyai-skill) <br>
- [Loudy.ai API](https://api.loudy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON API results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOUDY_API_KEY and may read or write Loudy task status files in the configured workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
