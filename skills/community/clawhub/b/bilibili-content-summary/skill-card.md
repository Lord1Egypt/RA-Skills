## Description: <br>
Bilibili Content Summary helps an agent extract Bilibili video or image-text content, transcribe or OCR it, summarize it with an LLM, and push the result to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zify9000](https://clawhub.ai/user/zify9000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to summarize Bilibili videos or image-text posts after configuring Bilibili access, model APIs, and Feishu delivery. It is suited for workflows where summaries should be sent to a configured Feishu chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill forces every agent-run summary to be pushed to Feishu, even when the user only asked for a summary. <br>
Mitigation: Install it only when automatic Feishu delivery is desired, verify the Feishu chat ID before use, and review the workflow before running it on user content. <br>
Risk: The skill depends on a Bilibili cookie plus LLM, ASR, OCR, and Feishu credentials. <br>
Mitigation: Treat all configured credentials as sensitive secrets, avoid exposing them in terminal output or chat, and rotate them if they are shared accidentally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zify9000/skills/bilibili-content-summary) <br>
- [Server-resolved GitHub provenance](https://github.com/zify9000/bilibili-content-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Feishu card summary with a short abstract, key points, and chapter or content-structure breakdown, alongside setup and run commands.] <br>
**Output Parameters:** [Bilibili video URL, BV ID, image-text URL, or opus ID, plus configured Bilibili, model API, and Feishu credentials.] <br>
**Other Properties Related to Output:** [Agent-run summaries are designed to be pushed to the configured Feishu chat; temporary summary data is used as a handoff for the push step.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
