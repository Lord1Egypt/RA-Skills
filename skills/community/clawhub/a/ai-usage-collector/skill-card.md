## Description: <br>
Extracts AI tool usage details from WeChat group text or screenshots and organizes relevant coworker activity into structured CSV records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmf515](https://clawhub.ai/user/gmf515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team AI adoption leads, HR or operations staff, and product managers use this skill to summarize coworker AI tool usage from group chat messages or screenshots into spreadsheet-ready records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat excerpts or screenshots may contain personal, unrelated, or confidential information. <br>
Mitigation: Provide only the minimum relevant messages, redact unrelated sensitive content, and share outputs only with authorized recipients. <br>
Risk: Extracted names, tools, and usage details may be incomplete or incorrect when source messages are ambiguous or OCR is imperfect. <br>
Mitigation: Review the CSV rows before sharing or pasting into Excel or Teams, and leave uncertain fields blank rather than adding unsupported details. <br>
Risk: CSV cell contents may behave unexpectedly when pasted into spreadsheet tools. <br>
Mitigation: Check generated CSV cells before pasting into Excel or Teams and quote fields that contain commas. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmf515/ai-usage-collector) <br>
- [Publisher profile](https://clawhub.ai/user/gmf515) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text CSV rows, optionally accompanied by a short Markdown note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV columns are name, AI tool, business scenario, value or action point, and notes; missing fields are left blank.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
