## Description: <br>
AI Fortune Teller provides entertainment-focused Bazi, tarot, daily fortune, K-line fortune chart, past-life portrait, and future-partner portrait workflows using MiniMax text and image APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackjls](https://clawhub.ai/user/jackjls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for entertainment-oriented fortune telling, tarot readings, personalized fortune summaries, and generated portrait or chart prompts. Agents can use it to format user inputs, call MiniMax-backed helpers, and return human-readable readings or generated image links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send names, birth details, user questions, and generated prompts to MiniMax. <br>
Mitigation: Treat inputs as personal data, avoid entering sensitive details, and run the skill only when MiniMax processing is acceptable for the use case. <br>
Risk: Helper scripts read API settings from the user's Clawd environment file and use the configured MiniMax host. <br>
Mitigation: Review the environment file before execution and verify MINIMAX_API_HOST points to the intended MiniMax endpoint. <br>
Risk: Generated K-line and portrait helpers can write reading records to /tmp JSON files. <br>
Mitigation: Delete generated /tmp result files after use if local retention of reading records is not desired. <br>
Risk: Fortune-telling and portrait outputs are entertainment content and may be misleading if used for important life, health, financial, or relationship decisions. <br>
Mitigation: Present outputs as entertainment and encourage users to rely on qualified professional advice for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackjls/ai-fortune-teller) <br>
- [Bazi prompt](references/bazi-prompt.md) <br>
- [Daily fortune prompt](references/daily-fortune-prompt.md) <br>
- [K-line generator](references/kline-generator.md) <br>
- [Tarot prompt](references/tarot-prompt.md) <br>
- [Usage examples](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, image URLs] <br>
**Output Format:** [Markdown or plain-text reports, shell command invocations, generated image URLs, and local JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some generated image links are described by the artifact as time-limited; helper scripts may write result JSON files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
