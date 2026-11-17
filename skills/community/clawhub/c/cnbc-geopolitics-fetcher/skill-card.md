## Description:

Fetches recent CNBC geopolitical news articles, extracts factual and market-impact details, and formats the results for Discord posting or file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimaschand29](https://clawhub.ai/user/dimaschand29)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to collect recent CNBC geopolitics articles, extract market-relevant facts, and deliver concise markdown briefings. It is aimed at users who monitor geopolitical events, energy markets, and prediction-market-relevant developments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a real-looking Discord webhook credential and examples that route posts through it.

Mitigation: Do not use the bundled webhook; revoke or replace it and supply any webhook through a local secret or private configuration mechanism.

Risk: Invoking the skill can send scraped CNBC article content and extracted facts to Discord.

Mitigation: Run the skill in an isolated Python environment, review the target webhook before execution, and use file output when external posting is not intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dimaschand29/skills/cnbc-geopolitics-fetcher)
- [CNBC article URL history](references/sent_urls.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown briefings and Discord messages with article URLs, market-impact text, and hard-fact bullets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a briefing file and splits Discord posts to fit Discord message-size limits.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
