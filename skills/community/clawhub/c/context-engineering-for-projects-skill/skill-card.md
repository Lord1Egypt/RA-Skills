## Description: <br>
Build or initialize team-style project context directories for context engineering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lywhlao2025](https://clawhub.ai/user/lywhlao2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scaffold project context workspaces linked to a local code directory, then populate navigation, module, agent, decision, and entrypoint documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects a user-provided local code directory and may capture sensitive project details in generated context files. <br>
Mitigation: Run it only against intended project folders and review generated documentation before sharing or relying on it. <br>
Risk: Generated memory, decision, and module files are persistent and could accidentally include secrets if users add them during follow-up population. <br>
Mitigation: Do not store secrets in the generated context workspace and scan or review the files before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lywhlao2025/context-engineering-for-projects-skill) <br>
- [Extraction rules reference](references/extraction-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated project context files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent context documentation under the selected target root and avoids overwriting existing files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
