## Description: <br>
会议纪要整理工具将会议录音转写稿整理为结构化会议纪要，并提取讨论要点、决策结论和行动项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inory0712](https://clawhub.ai/user/inory0712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn meeting transcripts into concise Chinese meeting minutes with topics, decisions, attendees, and action items. It is suited for transcript-to-minutes drafting after audio has already been converted to text by another tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts may contain secrets, regulated data, or unnecessary personal details. <br>
Mitigation: Confirm that transcript sharing is allowed and redact sensitive or unnecessary personal information before processing or distributing generated minutes. <br>
Risk: Generated minutes may misidentify attendees, dates, deadlines, or action owners when the transcript is ambiguous. <br>
Mitigation: Review the minutes before use and keep missing information marked as pending confirmation rather than guessing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/inory0712/auto-meeting-minutes) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown meeting minutes with sections and an action-item table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally produce per-person action item lists when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
