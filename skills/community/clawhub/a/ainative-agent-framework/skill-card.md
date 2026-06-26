## Description: <br>
Build multi-agent systems and swarms on AINative for orchestrating specialized OpenClaw agents, dispatching tasks, implementing agent communication, building handoff workflows, and collecting RLHF feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate AINative/OpenClaw agent workflows, dispatch tasks to specialized agents, connect to ACP sessions, call AINative APIs, and collect feedback for agent improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, memory entries, recall queries, RLHF feedback, session IDs, gateway tokens, and API keys may contain sensitive data. <br>
Mitigation: Redact secrets and regulated data before using the examples, and handle API keys and tokens as sensitive credentials. <br>
Risk: Delegated agent tasks and hosted API workflows can propose or perform actions that need human oversight. <br>
Mitigation: Review delegated tasks and generated outputs before running commands or applying changes. <br>


## Reference(s): <br>
- [AINative chat completions API endpoint](https://api.ainative.studio/v1/public/chat/completions) <br>
- [AINative memory remember API endpoint](https://api.ainative.studio/api/v1/public/memory/v2/remember) <br>
- [AINative memory recall API endpoint](https://api.ainative.studio/api/v1/public/memory/v2/recall) <br>
- [AINative RLHF feedback API endpoint](https://api.ainative.studio/api/v1/public/zerodb/rlhf/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may reference hosted APIs, local CLI commands, gateway tokens, API keys, memory, recall, RLHF feedback, and delegated agent tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
