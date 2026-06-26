## Description: <br>
Create agent company packages conforming to the Agent Companies specification (agentcompanies/v1) from scratch, from an existing repository, or from a skills collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlowne12](https://clawhub.ai/user/marlowne12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to interview users, analyze repositories when provided, and scaffold Agent Companies packages with company, agent, team, project, task, skill, README, license, and Paperclip configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local paths or repositories supplied for company generation, which may expose sensitive source content to the acting agent. <br>
Mitigation: Provide only repositories or local paths that are appropriate for the agent to inspect. <br>
Risk: Generated AGENTS.md, SKILL.md, .paperclip.yaml, and external source references may encode incorrect roles, unsafe configuration, or unsuitable dependency references. <br>
Mitigation: Review generated company files and external references before importing or running the company. <br>
Risk: Generated packages may include output locations or source references that do not match the user's intent. <br>
Mitigation: Confirm the output directory and source-reference strategy before writing or importing generated files. <br>


## Reference(s): <br>
- [Agent Companies Specification](https://agentcompanies.io/specification) <br>
- [Agent Companies Protocol Site](https://agentcompanies.io/) <br>
- [Agent Companies Specification Reference](references/companies-spec.md) <br>
- [Example Company Package](references/example-company.md) <br>
- [Creating a Company From an Existing Repository](references/from-repo-guide.md) <br>
- [Paperclip](https://github.com/paperclipai/paperclip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, YAML frontmatter, shell commands, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Agent Companies package files and asks for user confirmation before writing output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
