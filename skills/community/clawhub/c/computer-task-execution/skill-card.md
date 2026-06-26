## Description: <br>
Execute real user tasks across websites and local applications with a reliability-first strategy, choosing browser, official interface, hybrid, or UI automation paths based on reliability, verification, and user disruption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gift-is-coding](https://clawhub.ai/user/gift-is-coding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent must complete multi-step tasks in websites or local applications, including read-only inspection, draft preparation, GUI edits, messaging flows, and other verifiable computer-use work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad computer-task execution guidance can lead an agent toward live actions such as sending, submitting, deleting, posting, approvals, or bulk changes. <br>
Mitigation: Use only for explicit action-execution requests, give narrow task instructions, and require confirmation before any high-risk or bulk action. <br>
Risk: The bundled WeChat connectivity-test pattern could cause an agent to send a real message without clear user confirmation. <br>
Mitigation: Remove or edit the WeChat connectivity-test pattern before use, and require explicit recipient and message confirmation before sending. <br>
Risk: UI automation and background execution can target the wrong window, field, or account when focus or visible state is uncertain. <br>
Mitigation: Prefer browser or official interfaces when available, use foreground execution for critical high-risk steps, and verify completion from the target system before reporting success. <br>


## Reference(s): <br>
- [Pattern Memory Policy](references/pattern-memory.md) <br>
- [Site Pattern Templates](references/site-patterns/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline commands, code snippets, and verification notes as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task plans, execution-path choices, confirmation prompts, verification summaries, and updates to reusable pattern-memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
