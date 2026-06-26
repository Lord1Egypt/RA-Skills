## Description: <br>
Guides agents to read AIOS, OpenClaw, and Forguncy ontology files, invoke business-system commands or bindings through the approved CLI, and analyze live returned results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent must query live AIOS/OpenClaw/Forguncy business data, call ontology-defined commands or bindings, or perform system actions with results grounded in the current business system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live business-system access can execute write or destructive actions if routing, parameters, or user intent are wrong. <br>
Mitigation: Require explicit user confirmation for write or destructive actions, and verify the ontology-derived application, command, provider, SessionId, and jsonBody before running the CLI. <br>
Risk: Session identifier handling is ambiguous and may target the wrong live session. <br>
Mitigation: Normalize to one canonical session identifier field before use, and stop when the current SessionId is missing or ambiguous. <br>
Risk: Unsupported providers or incomplete ontology data can lead to incorrect business-system calls. <br>
Mitigation: Use the skill only in environments where the target AIOS/OpenClaw/Forguncy operations are understood, stop on unknown providers or incomplete ontology, and review generated commands before execution. <br>


## Reference(s): <br>
- [SKILL.md](SKILL.md) <br>
- [readme.md](readme.md) <br>
- [AIOS Application Invocation Rules](references/invoke-rules.md) <br>
- [AIOS Data Processing Rules](references/data-processing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized live-result analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite ontology files or entries used, identify servercommand versus binding calls, and state assumptions, missing fields, skipped data, and uncertainty.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
