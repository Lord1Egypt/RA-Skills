## Description: <br>
FactoriaGo helps agents support academic paper revision and resubmission by analyzing reviewer feedback, generating response letters, managing FactoriaGo projects and files, and guiding LaTeX compilation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyh2556406](https://clawhub.ai/user/gyh2556406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, PhD students, postdocs, and their agents use this skill to plan journal revisions, draft point-by-point reviewer responses, manage FactoriaGo projects and files, and compile LaTeX manuscripts through the FactoriaGo platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles account sessions and LLM API key setup, which can expose credentials if users paste secrets into chat or command-line history. <br>
Mitigation: Use secure web settings or scoped, revocable tokens where possible; keep session cookies in environment variables; avoid sharing API keys, passwords, or cookies in chat or command arguments. <br>
Risk: The skill can access manuscript content and reviewer feedback through authenticated FactoriaGo project APIs. <br>
Mitigation: Confirm the intended account, project, and file before each operation, and share only manuscript or review content needed for the requested revision task. <br>
Risk: File update workflows may alter LaTeX manuscript files or project tasks. <br>
Mitigation: Require a diff or preview before saving changes, keep manuscript backups or version history, and compile after edits to check for LaTeX errors. <br>


## Reference(s): <br>
- [FactoriaGo API Reference](references/api.md) <br>
- [FactoriaGo Revise & Resubmit Workflow](references/revision-workflow.md) <br>
- [Reviewer Response Letter Templates](references/reviewer-response.md) <br>
- [FactoriaGo Product Website](https://factoriago.com) <br>
- [FactoriaGo API Base](https://editor.factoriago.com/api) <br>
- [ClawHub Skill Listing](https://clawhub.ai/gyh2556406/factoriago) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated FactoriaGo API operations that read or update project metadata, manuscript files, revision tasks, LLM settings, and compilation status.] <br>

## Skill Version(s): <br>
2.9.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
