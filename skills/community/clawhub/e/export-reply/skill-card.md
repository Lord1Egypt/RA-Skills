## Description: <br>
Export Reply saves an agent reply or full conversation to local MD, TXT, HTML, PDF, or DOCX files with optional verbatim or condensed bilingual summary modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-owo](https://clawhub.ai/user/ryan-owo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who want a local record of AI work use this skill to export a selected reply or full conversation, either verbatim or as a condensed Chinese/English summary, into common document formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes chat content to local files, which may expose sensitive conversations if the destination is shared, synced, or otherwise accessible. <br>
Mitigation: Review the export path before confirming and avoid saving sensitive conversations to shared or synced folders. <br>
Risk: The skill can remember the last export destination and settings, which may cause later exports to reuse an unintended location. <br>
Mitigation: Confirm reused settings before export and clear ~/.export_reply_prefs.json when saved preferences are no longer wanted. <br>
Risk: PDF export may render content through a local browser. <br>
Mitigation: Use extra caution with PDF exports and choose MD, TXT, or HTML when browser-based rendering is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryan-owo/export-reply) <br>
- [Format Reference](references/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Local files in MD, TXT, HTML, PDF, DOCX, or all supported formats, with concise confirmation text from the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a user-selected local path and may remember the last export settings in ~/.export_reply_prefs.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
