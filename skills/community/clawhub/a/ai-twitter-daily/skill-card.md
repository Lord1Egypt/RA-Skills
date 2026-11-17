## Description:

Generate daily AI Twitter report from top AI researchers and companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danetteceola](https://clawhub.ai/user/danetteceola)

### License/Terms of Use:


## Use Case:

Developers, AI observers, and research teams use this skill to generate a Chinese-language daily summary of Twitter/X discussion from a fixed list of AI researchers and organizations. The report is produced through a configured LLM endpoint, so users should treat freshness and source coverage as dependent on that endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured API key and report prompt to a third-party LLM endpoint by default.

Mitigation: Use only a narrowly scoped or disposable key for the configured endpoint, and change GROK_API_URL to a trusted endpoint when appropriate.

Risk: The report may be an LLM-generated synthesis rather than an independently verified collection of current Twitter/X posts.

Mitigation: Review important claims against primary sources before using the report for decisions or publication.

## Reference(s):

- [Monitored X account list](artifact/references/users.txt)
- [ClawHub skill page](https://clawhub.ai/danetteceola/skills/ai-twitter-daily)
- [Default configured LLM endpoint](https://api.cheaprouter.club/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown-style report with tables and bullet points printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GROK_API_KEY and optionally GROK_API_URL and GROK_MODEL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
