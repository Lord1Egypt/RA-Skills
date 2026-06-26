## Description: <br>
飞书会议总结技能 - 读取飞书会议纪要，生成结构化总结，沉淀知识，支持搜索 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YannBoy](https://clawhub.ai/user/YannBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn Feishu meeting records into structured meeting summaries, follow-up items, and reusable knowledge notes. It is intended for workflows where meeting content can be read from Feishu and saved back into a configured Feishu workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts, summaries, and source links may contain sensitive information and are stored in the configured Feishu workspace. <br>
Mitigation: Use a restricted meetings folder, verify folder permissions, and avoid highly confidential meetings unless retention and access controls are appropriate. <br>
Risk: The skill depends on a Feishu plugin and Feishu workspace access to read and write meeting content. <br>
Mitigation: Install and use the Feishu plugin only when trusted, and confirm the configured workspace locations before saving generated summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YannBoy/feishu-meeting-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown meeting summaries, Feishu document links, and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu meeting records and configured workspace folders; stores generated summaries and retained source links in Feishu.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
