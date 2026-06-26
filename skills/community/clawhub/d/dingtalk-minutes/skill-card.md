## Description: <br>
Automatically organizes DingTalk and Feishu meeting records by merging related transcripts, extracting participants, core topics, key decisions, and action items, then archiving the minutes to a configured directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pwu0125](https://clawhub.ai/user/pwu0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn exported DingTalk or Feishu transcript text files into structured Markdown meeting minutes. It is useful for organizing local meeting archives with participants, agenda topics, decisions, action items, and category-based filing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local meeting-record folders that may contain confidential meeting content. <br>
Mitigation: Use a dedicated transcript input folder containing only records intended for processing, and restrict archive access when meetings are confidential. <br>
Risk: Generated minutes may omit context, misclassify related meetings, or produce incorrect decisions or action items. <br>
Mitigation: Review generated or updated minutes before sharing them or relying on them for follow-up work. <br>
Risk: The skill writes derived summaries under ./memory/meetings/, which may retain sensitive information from the source transcripts. <br>
Mitigation: Apply the same retention and access controls to the generated archive as to the original meeting records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pwu0125/dingtalk-minutes) <br>
- [README.en.md](artifact/README.en.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown meeting minutes saved as local .md files with a short processing report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads configured local transcript folders and writes generated minutes under ./memory/meetings/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
