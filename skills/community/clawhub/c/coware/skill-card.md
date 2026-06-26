## Description: <br>
Coware Living Specs syncs shared API specs for multi-agent coding teams when a project uses Coware or needs team, API, interface, or merge-conflict alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shitianfang](https://clawhub.ai/user/shitianfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to keep AI coding agents aligned with shared interface and API specs before, during, and after code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote setup guide and project sync scripts can influence account, project, and upload actions. <br>
Mitigation: Before first use, have the agent show the fetched setup guide, confirm any login, project, or invite-code steps, and inspect the .coware Node scripts in the repository. <br>
Risk: Shared specs may include secrets or sensitive internal architecture. <br>
Mitigation: Review spec contents before syncing and avoid publishing credentials, tokens, private endpoints, or sensitive architecture details. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shitianfang/coware) <br>
- [Coware setup guide](https://coware.team/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs agents to read local Coware specs and may instruct them to run project-local sync scripts when Coware is initialized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
