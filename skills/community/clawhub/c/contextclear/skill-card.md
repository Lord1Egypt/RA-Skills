## Description: <br>
ContextClear helps agents report wellness, cost, performance, memory, context recovery, and quality signals to the ContextClear API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfedorov](https://clawhub.ai/user/mfedorov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ContextClear to connect agents to ContextClear for metric reporting, context snapshots, recovery briefings, sticky notes, memory curation, alerts, and optional workspace backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send broad agent memory, task history, repository metadata, file metadata, and workspace context to an external ContextClear service. <br>
Mitigation: Install only when that data sharing is intended; redact sensitive context, use allowlists, and confirm service retention and access controls before enabling snapshots or vault backup. <br>
Risk: The artifact shows API keys configured in agent memory files and command examples, which can expose credentials if those files are shared or backed up. <br>
Mitigation: Store credentials in environment variables or a secret manager, and avoid placing API keys in AGENTS.md, HEARTBEAT.md, or other persisted memory files. <br>
Risk: The setup workflow can add persistent instructions that make agents recover context, report snapshots, and optionally back up identity and memory files. <br>
Mitigation: Review the generated file changes before relying on them, disable vault backup unless explicitly needed, and keep backup scope limited to approved files. <br>


## Reference(s): <br>
- [ContextClear API Reference](references/api.md) <br>
- [ContextClear Dashboard](https://contextclear.com) <br>
- [ContextClear API](https://api.contextclear.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Code] <br>
**Output Format:** [Markdown guidance with bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup and reporting scripts that can append ContextClear recovery and snapshot instructions to AGENTS.md and HEARTBEAT.md when run.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
