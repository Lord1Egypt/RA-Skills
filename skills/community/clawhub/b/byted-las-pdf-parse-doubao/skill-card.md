## Description: <br>
Parses and reads PDF documents into structured Markdown text using Volcengine LAS Doubao AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to submit PDFs to Volcengine LAS, estimate per-page cost, poll asynchronous parsing jobs, and return extracted Markdown, page details, tables, charts, and OCR text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install remote executable SDK code from a hosted source. <br>
Mitigation: Install only after reviewing and trusting the hosted SDK source; prefer a revised release that pins or bundles the SDK and asks before downloading executable code. <br>
Risk: PDF files and extracted content are sent to the Volcengine LAS service. <br>
Mitigation: Use only for data approved for that provider and document privacy handling before processing sensitive PDFs. <br>
Risk: Background polling can run without a built-in stop control. <br>
Mitigation: Use bounded polling windows where possible and prefer a revised release with an explicit timeout or stop control. <br>
Risk: The skill requires sensitive credentials. <br>
Mitigation: Provide credentials through environment variables or approved secret handling and avoid writing API keys into prompts, logs, or committed files. <br>


## Reference(s): <br>
- [LAS PDF Parse API Reference](references/api.md) <br>
- [LAS PDF Parse Pricing Reference](references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-las-pdf-parse-doubao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task IDs, local output paths, Markdown previews, page-detail JSON guidance, and billing notices.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
