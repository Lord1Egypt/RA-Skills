## Description: <br>
Installs a curated set of OpenClaw skills for new users, server setup, or environment recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianduoduo1422608857](https://clawhub.ai/user/qianduoduo1422608857) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to initialize a new OpenClaw environment, deploy a server quickly, or restore a working skill set by running an installer for selected skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an installation shell script that changes the OpenClaw environment. <br>
Mitigation: Review install.sh before execution and run it only when intentionally initializing or restoring the listed skill set. <br>
Risk: The installer adds multiple skills and may require later environment cleanup if the result is not desired. <br>
Mitigation: Confirm the interactive prompt, understand which skills will be installed, and keep a path to undo or restore the affected OpenClaw environment. <br>
Risk: Activation and consent boundaries are broad for host-changing setup behavior. <br>
Mitigation: Require explicit user confirmation before running the shell script and avoid automatic execution from vague install requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qianduoduo1422608857/essential-skills-installer) <br>
- [Tavily](https://tavily.com) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with a bash command and shell script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs an interactive install script that invokes the skillhub CLI and reports installed or failed skills.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
