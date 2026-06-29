## Description: <br>
Guides agents through exporting and locally analyzing ChatGPT web conversations and Gemini web activity exports, including JSON, HTML, and cross-platform normalization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoqing404](https://clawhub.ai/user/shaoqing404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and individual users use this skill to help export ChatGPT or Gemini web chat histories, verify export structure, convert records into searchable formats, and produce privacy-aware summaries or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ChatGPT and Gemini export files can contain private conversations, account details, feedback, and other personal information. <br>
Mitigation: Keep exports local, remove them from the workspace after analysis, and redact personal identifiers in reports. <br>
Risk: Gemini exports may include other Google activity in addition to Gemini chat content. <br>
Mitigation: Inspect the Takeout contents before analysis and limit processing to the intended Gemini export files. <br>
Risk: Large export files can be slow or memory-intensive to inspect in one pass. <br>
Mitigation: Use targeted jq, grep, or chunked processing and avoid dumping full exports into chat or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/gemini-openai-chat-export-analyze) <br>
- [Server-resolved GitHub source](https://github.com/shaoqing404/ai-chat-timeline-skills/tree/main/skills/gemini-openai-chat-export-analyze) <br>
- [Publisher profile](https://clawhub.ai/user/shaoqing404) <br>
- [ChatGPT web app](https://chatgpt.com) <br>
- [Google account data page](https://myaccount.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash, jq, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process local JSON and HTML chat export files; reports should redact personal identifiers by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
