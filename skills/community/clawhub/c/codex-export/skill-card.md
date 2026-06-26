## Description: <br>
Exports Codex CLI or Codex Desktop sessions to Markdown transcripts, with listing and brief modes for reviewing or sharing past conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinghan23](https://clawhub.ai/user/jinghan23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to find a local Codex session and export it as Markdown for review, sharing, or archival. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported transcripts may include sensitive prompts, workspace paths, tool calls, and tool outputs from local Codex session history. <br>
Mitigation: Export only sessions intended for review or sharing, use brief mode when tool details are unnecessary, and review or redact Markdown before distribution. <br>
Risk: The skill reads past Codex session files from the local machine. <br>
Mitigation: Run it only when local session export is the intended task and confirm the selected session ID and output destination before exporting. <br>


## Reference(s): <br>
- [OpenAI Codex issue 2880](https://github.com/openai/codex/issues/2880) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown transcript or terminal listing produced by a Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default exports include tool calls and outputs; brief mode limits output to user and assistant messages.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
