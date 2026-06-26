## Description: <br>
Extracts structured personal memories from ChatGPT export data into timelines, people profiles, and thematic records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyresearch](https://clawhub.ai/user/cyresearch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert their own ChatGPT export into a searchable personal memory archive. The agent reads exported conversations in batches, writes timeline files, and maintains people and topic records for later review or reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated archive can contain sensitive personal, third-party, or secret information from a user's ChatGPT history. <br>
Mitigation: Store outputs in a private or encrypted folder, avoid cloud-synced or Git-tracked locations unless intentional, and redact sensitive details before sharing the archive or giving it to another AI assistant. <br>
Risk: Large exports may lead an agent to produce shallow, incomplete, or false-completion summaries. <br>
Mitigation: Process the export in reviewable batches, verify each batch against the raw extracted conversations, and redo shallow sections before continuing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyresearch/chatgpt-memory-extraction) <br>
- [Output Format Specification](references/output-format.md) <br>
- [Quality Rules](references/quality-rules.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ChatGPT export](https://chat.openai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and plaintext extracted conversations, with shell commands for running the extraction script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timeline, people, topics, meta, and raw conversation files from a user-provided ChatGPT export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
