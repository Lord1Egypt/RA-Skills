## Description: <br>
This skill helps users submit and query batch image and video generation tasks through a local DYU client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaolou888](https://clawhub.ai/user/xiaolou888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to drive a locally running DYU media-generation client from conversation, submit single or batch image/video jobs, and query task status or results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, private URLs, or prior task history may be forwarded by the local DYU client to configured AI services. <br>
Mitigation: Do not submit secrets, confidential images, private internal URLs, or sensitive task history unless that external AI-service flow is acceptable. <br>
Risk: The skill relies on the local DYU client and its configured gateway/SK. <br>
Mitigation: Install and use the skill only when the DYU client and its gateway configuration are trusted. <br>
Risk: Batch generation can submit many media jobs at once. <br>
Mitigation: Review large batch prompts, reference images, and task counts before submission. <br>


## Reference(s): <br>
- [Video generation interface](references/video_generate.md) <br>
- [Image generation interface](references/image_generate.md) <br>
- [Task query interface](references/task_query.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiaolou888/ai-productivity-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/xiaolou888) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with JSON-like task payloads, Python snippets, task IDs, and result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include task IDs, one-shot status summaries, batch result tables, and verbatim result URLs returned by the local client.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
