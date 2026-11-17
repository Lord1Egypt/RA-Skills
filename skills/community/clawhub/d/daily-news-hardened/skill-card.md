## Description:

Fetch top news from Baidu, Google, and other sources daily.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a Python news script and return a daily list of trending headlines from Baidu, Google Trends, and similar sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a Python script and depends on external Python packages.

Mitigation: Install and run it in a virtual environment or other low-privilege sandbox, and pin and review dependency versions before use.

Risk: The script makes outbound requests to external news and trends sources and returns untrusted headline text.

Mitigation: Treat returned headlines as untrusted external content and avoid using them as instructions for unrelated agent actions.

Risk: Unrelated shell commands, file operations, or repeated autonomous retries could expand the skill's operational risk.

Mitigation: Limit execution to the declared news script and dependency installation, run the script at most once per user request, and require user direction after failures.

## Reference(s):

- [Daily News Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/daily-news-hardened)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/daily-news)
- [Baidu Realtime Hot Board](https://top.baidu.com/board?tab=realtime)
- [Google Trends Daily RSS](https://trends.google.com/trends/trendingsearches/daily/rss?geo=US)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown containing the script output and concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a Python script and returns a single daily headline stream; dependencies are declared in requirements.txt.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
