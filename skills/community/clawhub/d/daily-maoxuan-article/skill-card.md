## Description: <br>
每日毛泽东选集文章推送。AI深度解读，支持 Obsidian 文档生成和 Telegram 推送。75篇文章库，每日一篇。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi488](https://clawhub.ai/user/wudi488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal knowledge-management users use this skill to generate a daily Chinese reading note from a 75-article Mao Zedong Selected Works corpus, save it as an Obsidian Markdown document, and optionally send it to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated notes can be sent to the configured Telegram chat. <br>
Mitigation: Test with --chat or --no-send first, then confirm TELEGRAM_CHAT_ID points to the intended private chat before enabling Telegram delivery. <br>
Risk: Generated Markdown files are written under the configured Obsidian output directory. <br>
Mitigation: Set MAOXUAN_OUTPUT_DIR to the intended notes folder and verify file output before scheduling unattended runs. <br>
Risk: The skill depends on sensitive API and bot credentials. <br>
Mitigation: Provide DEEPSEEK_API_KEY, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID through environment variables and avoid committing real credential values. <br>
Risk: Persistent daily automation can repeatedly publish unwanted content if configured prematurely. <br>
Mitigation: Enable cron only after reviewing sample output and confirming the delivery channel and output path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wudi488/daily-maoxuan-article) <br>
- [README](README.md) <br>
- [Mao article database](references/mao-articles.md) <br>
- [Mao expansions](references/mao-expansions.md) <br>
- [Mao quotes](references/mao-quotes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, image files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, Telegram text messages, optional PNG images, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Selects one article deterministically by date; can run in chat-only, no-send, or simple mode.] <br>

## Skill Version(s): <br>
9.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
