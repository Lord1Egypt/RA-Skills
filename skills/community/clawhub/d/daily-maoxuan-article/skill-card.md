## Description:

每日毛泽东选集文章推送。AI深度解读，支持 Obsidian 文档生成和 Telegram 推送。75篇文章库，每日一篇。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi488](https://clawhub.ai/user/wudi488)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily Markdown article interpretation from a 75-article Mao Zedong anthology library, optionally save it to Obsidian, and send it through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional image generator can execute another local script with the user's full environment, including unrelated secrets.

Mitigation: Avoid SEEDREAM_SCRIPT and the optional image generator unless the referenced di-seedream-gen script is trusted; run with a minimal environment when image generation is needed.

Risk: Daily scheduled delivery can send content or write files to the wrong destination if Telegram or output settings are misconfigured.

Mitigation: Verify TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN, and MAOXUAN_OUTPUT_DIR before enabling scheduled runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wudi488/skills/daily-maoxuan-article)
- [Publisher Profile](https://clawhub.ai/user/wudi488)
- [Mao Article Database](references/mao-articles.md)
- [Mao Article Expansions](references/mao-expansions.md)
- [Mao Quotes](references/mao-quotes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, Telegram messages, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write dated Markdown files to the configured Obsidian output directory and may send messages to the configured Telegram chat.]

## Skill Version(s):

9.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
