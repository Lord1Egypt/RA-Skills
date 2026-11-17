## Description:

Generates Chinese daily briefing Markdown from Tavily keyword searches and can print the briefing or save it to a local file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to create concise Chinese daily industry or topic briefings from search keywords, then review the generated Markdown or save it as a local briefing file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package advertises RSS ingestion, scheduled delivery, and enterprise messaging push behavior that is not implemented in the shipped artifact.

Mitigation: Use the shipped Tavily keyword briefing script as the supported behavior unless RSS, scheduling, or push features are added, documented, and reviewed separately.

Risk: Search topics are sent to Tavily and require a TAVILY_API_KEY.

Mitigation: Use scoped credentials, avoid sensitive query terms, and review generated links and summaries before sharing the briefing.

Risk: The script writes to the user-supplied output path when --output is provided.

Mitigation: Choose an intended local Markdown path and review existing files before running commands that save output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/skills/daily-briefing-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown briefing text, optionally written to a local .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TAVILY_API_KEY for live Tavily search; --sources selects comma-separated topics and --max-items limits briefing entries.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
