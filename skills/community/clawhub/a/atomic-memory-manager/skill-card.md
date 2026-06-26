## Description: <br>
Helps OpenClaw agents retrieve and persist workspace memory using MEMORY.md, daily memory notes, memory_search, and memory_get. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omaression](https://clawhub.ai/user/omaression) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when agents need to answer from prior workspace memory, record durable preferences or decisions, or explain how workspace memory should be used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist preferences, decisions, or session context into workspace memory files. <br>
Mitigation: Do not ask the agent to store secrets or sensitive personal data unless that persistence is intentional. <br>
Risk: Retrieved memory can be stale or incomplete. <br>
Mitigation: Use the skill's retrieval rules to cite memory sources when useful, separate memory facts from inference, and flag stale or unavailable memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omaression/atomic-memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and file-backed memory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read retrieved memory snippets and write concise persistent notes when the user asks to remember durable information.] <br>

## Skill Version(s): <br>
1.0.0-alpha (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
