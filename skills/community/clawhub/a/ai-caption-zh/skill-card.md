## Description: <br>
AI 字幕 helps agents use Sparki to add clean, readable captions to videos and prepare caption-first short-form edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, editors, and operators use this skill to add clear captions to spoken or explanatory videos so they remain understandable without sound. Agents can run the Sparki CLI workflow for local video upload, prompt-driven editing, status polling, and result download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos and prompts are sent to Sparki for processing. <br>
Mitigation: Use the skill only for videos and prompts that are appropriate to send to Sparki, and confirm the destination service before upload. <br>
Risk: The setup workflow can store a Sparki API key and project history under $HOME/.openclaw/config. <br>
Mitigation: Prefer SPARKI_API_KEY from the environment on shared machines, and protect or clear sparki.json and sparki_history.json when needed. <br>
Risk: A custom Sparki base URL can redirect uploads, prompts, and credentials to a different service. <br>
Mitigation: Do not configure a custom base URL unless the operator trusts that endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/ai-caption-zh) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki Telegram upload link](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Sparki CLI may produce task IDs, asset metadata, result URLs, local MP4 file paths, and delivery hints.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata, SKILL.md frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
