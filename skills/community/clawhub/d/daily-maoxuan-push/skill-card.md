## Description: <br>
每日毛选语录硬核推送：生成每日《毛泽东选集》语录 Markdown 文档，调用 AI 生成六章结构的深度解读，并可推送到 Obsidian 和 Telegram。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi488](https://clawhub.ai/user/wudi488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate a daily Mao-selected-works quote workflow: select a quote, generate a Markdown note with AI-assisted analysis, save it to a local Obsidian-style directory, and optionally send a Telegram update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive DeepSeek and Telegram credentials for normal operation. <br>
Mitigation: Use dedicated, rotatable credentials and provide them through environment variables rather than editing source files. <br>
Risk: The skill can create local Markdown files and send Telegram messages automatically when scheduled. <br>
Mitigation: Run `python3 scripts/generate_daily.py --test` or `--no-send` before enabling delivery, verify the configured output directory, and create the cron job only when daily automation is intended. <br>
Risk: README claims about image and voice generation may be stale for this release. <br>
Mitigation: Treat image and voice behavior as unverified unless separately tested in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wudi488/daily-maoxuan-push) <br>
- [README.md](artifact/README.md) <br>
- [references/config.json](artifact/references/config.json) <br>
- [references/maoxuan_quotes.json](artifact/references/maoxuan_quotes.json) <br>
- [references/template.md](artifact/references/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and messaging text with optional shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write dated Markdown notes to a configured local output directory and may send Telegram messages when credentials are configured.] <br>

## Skill Version(s): <br>
5.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
