## Description: <br>
AI Dev Runtime gives agents tools for code reading, search, editing, terminal execution, tests, bug fixing, batch tasks, and codebase analysis with hybrid search and learning memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sammytan](https://clawhub.ai/user/sammytan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate development tasks to an AI Dev Runtime server, including file inspection, semantic and keyword search, edits, terminal commands, test runs, bug fixes, and codebase analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to an external runtime with broad file-editing and terminal-execution authority. <br>
Mitigation: Install only when the AI Dev Runtime endpoint is trusted, run with least privilege, and review edits and terminal commands before execution. <br>
Risk: Runtime memory and API key handling may affect confidentiality if the endpoint is not controlled. <br>
Mitigation: Verify the runtime's learning memory behavior and API key handling before using sensitive code, credentials, or repositories. <br>


## Reference(s): <br>
- [AI Dev Runtime on ClawHub](https://clawhub.ai/sammytan/ai-dev-runtime) <br>
- [AI Dev Runtime homepage from metadata](https://github.com/your-org/AiDevRuntime) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and tool-call results with code, command, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform file edits and terminal commands through a configured AI Dev Runtime endpoint.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
