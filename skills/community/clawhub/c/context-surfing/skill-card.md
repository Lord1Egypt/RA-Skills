## Description: <br>
Monitors context window health during multi-step agent sessions, helps the agent stay grounded in current intent and project context, and guides clean handoff when context quality degrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pskoett](https://clawhub.ai/user/pskoett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill during long-running or complex agent work to monitor context quality, re-anchor against task and project evidence, and preserve continuity through handoff files when drift is detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist detailed task, plan, prompt, and session information in local handoff files. <br>
Mitigation: Use it only in sessions where local handoff artifacts are acceptable, and require redaction and cleanup rules before use with secrets, credentials, customer data, incident details, or proprietary prompts. <br>
Risk: The skill can activate automatically during broad multi-step work, which may add context-continuity behavior without an explicit per-step approval. <br>
Mitigation: Review the skill before deployment and define when automatic context checks and handoff creation are allowed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pskoett/context-surfing) <br>
- [Entire CLI](https://github.com/entireio/cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local handoff markdown files for session continuity when context drift is detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
