## Description:

每日毛选语录硬核推送。AI深度解读（六章结构/2000+字），拒绝鸡汤、直击本质，配图+语音，Obsidian+Telegram多渠道推送。思想操作系统，每天强制认知重启。v5.0升级：硬核解读协议，阶级分析+组织策略+当代丛林生存指南。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi488](https://clawhub.ai/user/wudi488)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure this skill to generate a daily Mao Selected Works quote note, produce optional long-form AI commentary, save the result as Markdown, and push the daily message to configured channels such as Telegram or Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles messaging credentials and can send generated content to Telegram or Feishu.

Mitigation: Use a dedicated bot or app credential, scope the destination chat carefully, keep tokens in environment variables, and rotate credentials if logs may have exposed failed request details.

Risk: The skill can run as unattended daily automation and write Markdown files to a configured local directory.

Mitigation: Run with --no-send or --dry-run first, restrict MAOXUAN_OUTPUT_DIR or the configured output directory, and avoid running install.sh with elevated privileges.

Risk: Generated historical or political commentary may be inaccurate, misleading, or unsuitable for a target audience.

Mitigation: Review generated Markdown before broad distribution and treat AI commentary as draft content rather than a verified historical source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wudi488/skills/daily-maoxuan-push)
- [Publisher profile](https://clawhub.ai/user/wudi488)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Quote reference data](artifact/references/maoxuan_quotes.json)
- [Runtime configuration](artifact/references/config.json)
- [Output template](artifact/references/template.md)
- [DeepSeek API endpoint](https://api.deepseek.com)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown files, messaging text, and concise command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write dated Markdown files to a configured local output directory and may send generated content through user-configured messaging credentials.]

## Skill Version(s):

5.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
