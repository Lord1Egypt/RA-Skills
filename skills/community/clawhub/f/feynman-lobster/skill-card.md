## Description: <br>
feynman-lobster is a project-driven learning companion that reads user-provided code and notes, manages learning contracts, and uses Feynman-style questioning to help users learn while building. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lysandre001](https://clawhub.ai/user/lysandre001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and learners use this skill to turn active projects into guided learning contracts. It tracks progress, reads specified project or note paths as context, asks targeted Feynman-style questions, and can launch a local progress panel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided project and note paths and stores learning state that may contain sensitive workspace context. <br>
Mitigation: Only add intended local paths, avoid including secrets in learning resources, and review generated contracts, profile notes, and contract memory files. <br>
Risk: The optional local dashboard and API handle private learning data with weak browser isolation. <br>
Mitigation: Run the panel only when needed, keep it bound to localhost, avoid untrusted contract text or URLs until dashboard escaping is fixed, and stop the local processes when finished. <br>
Risk: Setup and panel scripts start local processes and perform local file side effects. <br>
Mitigation: Review scripts before execution and monitor the generated files and background processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lysandre001/feynman-lobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text conversational guidance with optional shell commands and local panel instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning state files such as contracts, user profile notes, and contract memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
