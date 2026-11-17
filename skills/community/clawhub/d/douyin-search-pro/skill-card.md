## Description:

Searches Douyin viral works by keyword and optional date range, then returns structured engagement data and links for content trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, MCN teams, brand operators, growth teams, and marketing teams use this skill to search Douyin content trends, compare engagement metrics, and monitor keywords for daily trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and date filters are sent to RedFox using REDFOX_API_KEY.

Mitigation: Use a scoped, revocable RedFox key and avoid hard-coding or exposing it in prompts, logs, code, or output files.

Risk: Daily subscription guidance may create a persistent scheduled command with unsafe keyword interpolation.

Mitigation: Prefer a platform scheduler or fixed runner with safe argument handling, clear removal steps, and least-privilege execution.

Risk: The server security verdict is suspicious because subscription setup needs review before use.

Mitigation: Review subscription commands and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/douyin-search-pro)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables with clickable links, plus occasional shell command snippets and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends search keywords and optional date filters to RedFox.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
