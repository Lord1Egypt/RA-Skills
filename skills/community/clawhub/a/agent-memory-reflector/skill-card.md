## Description: <br>
Enables AI agents to review past decisions, identify reasoning loops, and produce self-improvement insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building AI agent workflows use this skill to log prompts, responses, and metadata, then generate local reflection reports that highlight repeated queries, uncertainty signals, self-corrections, and improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, responses, metadata, and reflection reports may be saved as plaintext local files. <br>
Mitigation: Avoid logging secrets, credentials, private conversations, or proprietary context unless redaction, restrictive file permissions, encryption, and a retention or deletion process are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/agent-memory-reflector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and plaintext CLI output; the bundled Python tool writes JSONL logs and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores interaction history and reflection reports locally under .agent_memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
