## Description: <br>
Analyze conversation transcripts: decisions, action items, dates, people, executive summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to turn pasted transcripts, chat logs, email threads, meeting notes, or referenced transcript files into concise structured reports. It is intended for extracting summaries, decisions, action items, dates, people, open questions, and risks from conversation text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation transcripts may contain confidential, personal, or business-sensitive information. <br>
Mitigation: Only provide transcripts the agent is allowed to read, and avoid saving reports unless a written output is intended. <br>
Risk: The skill requests file-read and memory-read permissions that may expose transcript files or existing memory when enabled. <br>
Mitigation: Review file paths and memory access before invocation, and disable unnecessary permissions in restricted environments. <br>
Risk: Extracted decisions, action items, dates, people, or risks may be incomplete or inaccurate for ambiguous conversations. <br>
Mitigation: Review the generated report against the source transcript before relying on it for commitments or follow-up. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/andreataide86/conversa-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bullets or tables depending on the conversation format; long inputs may be summarized before extraction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
