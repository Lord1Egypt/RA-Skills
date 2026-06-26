## Description: <br>
AI Agent Psychologist is a manual-trigger skill for AI agents to run self-alignment checks, dialogue diagnosis, structured introspection, intervention prompts, health checkups, and local Markdown journals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prompt agents through structured self-checks and to generate local Markdown records for diagnosis, checkups, journals, and introspection logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter an agent's response style when a manual trigger phrase is used. <br>
Mitigation: Use explicit trigger phrases intentionally and avoid broad trigger words in casual conversation. <br>
Risk: Local diagnosis, checkup, journal, and introspection files may contain sensitive conversation details. <br>
Mitigation: Periodically review, protect, or delete the local journal and log files according to the user's retention needs. <br>
Risk: The skill relies on reflective prompting and conversation-context reasoning, not direct access to model internals. <br>
Mitigation: Treat self-check reports as guidance for review rather than as authoritative measurements of internal model state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moroiser/ai-agent-psychologist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and logs, shell-script output, and structured prompt guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written under the local ai-agent-psychologist workspace directory when helper scripts are invoked.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
