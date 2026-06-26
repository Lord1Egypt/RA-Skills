## Description: <br>
Summarizes Feishu group chats for a requested time range, reports activity statistics, and creates a Feishu document containing both the summary and complete text-message records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glory904649854](https://clawhub.ai/user/glory904649854) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to export and summarize authorized Feishu group chat history over a chosen time range, including active-member counts, recent-message previews, and complete text-message records in a Feishu document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exports sensitive Feishu group chat history, participant IDs, nicknames, timestamps, and message contents into persistent documents. <br>
Mitigation: Run it only for groups where export is authorized, restrict the Feishu app to the required permissions, and verify the created document's sharing settings. <br>
Risk: The script passes Feishu credentials to a local feishu-docs helper program. <br>
Mitigation: Confirm the feishu-docs CLI source and integrity before use, and provide credentials through a least-privilege Feishu app. <br>
Risk: Generated temporary or backup Markdown files may retain chat records locally. <br>
Mitigation: Delete tmp_chat_summary.md and any chat_summary_*.md backup files after confirming the Feishu document output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glory904649854/catfee-feishu-recorder) <br>
- [Publisher profile](https://clawhub.ai/user/glory904649854) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Console text, Markdown summaries, and Feishu document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET environment variables, a chat_id, and a time-range argument.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
