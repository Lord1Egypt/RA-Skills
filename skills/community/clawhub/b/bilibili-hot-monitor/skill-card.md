## Description:

Generates and emails daily Bilibili popular-video reports with subtitle-based AI summaries and content-performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobzwj](https://clawhub.ai/user/jacobzwj)

### License/Terms of Use:

MIT License

## Use Case:

External users and content operators use this skill to monitor Bilibili trending videos, generate a structured daily Markdown report, optionally enrich it with OpenRouter-based analysis, and email the result to configured recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store reusable Bilibili cookies, an OpenRouter API key, and SMTP credentials in plaintext configuration.

Mitigation: Prefer environment variables or a secret manager, keep generated configuration local, and avoid passing secrets on the command line.

Risk: SMTP credentials allow the skill to send email to configured recipients.

Mitigation: Use an app-specific email password and review recipient addresses before running the send step.

Risk: Video titles, metadata, subtitles, summaries, and generated reports may be shared with OpenRouter or email recipients.

Mitigation: Disable AI enrichment when content should not be sent to OpenRouter and verify report contents before emailing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacobzwj/skills/bilibili-hot-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/jacobzwj)
- [Bilibili API WBI signature reference](https://socialsisteryi.github.io/bilibili-API-collect/docs/misc/sign/wbi.html)
- [Bilibili video summary API reference](https://socialsisteryi.github.io/bilibili-API-collect/docs/video/summary.html)
- [OpenRouter API keys](https://openrouter.ai/keys)
- [Google app passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, optional HTML email, and command-line setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local JSON configuration file, write a report file, call Bilibili and OpenRouter over HTTPS, and send email through SMTP.]

## Skill Version(s):

1.0.21 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
