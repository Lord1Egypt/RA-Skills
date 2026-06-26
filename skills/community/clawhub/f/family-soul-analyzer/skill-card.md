## Description: <br>
Family Soul Analyzer turns exported family or group chat logs into a collective soul document and member persona files for use by an AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengury](https://clawhub.ai/user/zengury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to analyze exported chat records, extract relationship and behavior patterns, and generate Markdown soul/persona files that can guide downstream agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact bundles sensitive chat data. <br>
Mitigation: Remove bundled raw chat exports before installation or redistribution, and only process chat records with consent from all relevant participants. <br>
Risk: Private chat content may be sent to external AI services. <br>
Mitigation: Confirm the configured provider and data handling terms before use; avoid processing confidential chats unless the provider and retention policy are acceptable. <br>
Risk: The artifact includes hardcoded third-party API credential paths or values. <br>
Mitigation: Remove hardcoded credentials, rotate any exposed keys, and require credentials to come from environment variables or a managed secret store. <br>
Risk: The pipeline may not reliably honor user-supplied input and output paths. <br>
Mitigation: Run in an isolated working directory, verify the actual input and output locations before processing, and delete generated outputs and caches after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengury/family-soul-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/zengury) <br>
- [Skill README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and agent-readable progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces soul.md and persona Markdown files; execution may call external AI services depending on configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
