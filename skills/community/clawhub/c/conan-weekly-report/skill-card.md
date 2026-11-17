## Description:

Generates a weekly Detective Conan anime report by searching public web results and organizing recent episodes, storyline updates, specials, character news, production notes, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hubertsing](https://clawhub.ai/user/hubertsing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and entertainment fans use this skill to receive a concise weekly Markdown summary of recent Detective Conan anime developments. OpenClaw users can run it manually or schedule it to save reports locally and optionally deliver them through a configured webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs can repeatedly create local Markdown reports under the skill's reports directory.

Mitigation: Enable the weekly cron job only when recurring local report files are desired, and periodically review or clean the reports directory.

Risk: Webhook delivery can send generated report content to an external destination when REPORT_WEBHOOK_URL is configured.

Mitigation: Set REPORT_WEBHOOK_URL only for trusted endpoints, prefer HTTPS, and leave it unset when external delivery is not needed.

Risk: Public web searches may return incomplete, stale, or unavailable results.

Mitigation: Review source links in the generated report and consult official or trusted anime information channels before relying on the summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hubertsing/skills/conan-weekly-report)
- [Bilibili Detective Conan page](https://www.bilibili.com/bangumi/media/md2819)
- [Baidu Baike Detective Conan page](https://baike.baidu.com/item/名侦探柯南/3469662)
- [Wikipedia Detective Conan page](https://zh.wikipedia.org/wiki/名侦探柯南)
- [DuckDuckGo HTML Search](https://html.duckduckgo.com/html/)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown report text saved to a local file, printed to the console, and optionally posted as JSON text to a webhook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates reports named conan-report-YYYY-MM-DD.md under the skill's reports directory; webhook delivery only occurs when REPORT_WEBHOOK_URL is configured.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
