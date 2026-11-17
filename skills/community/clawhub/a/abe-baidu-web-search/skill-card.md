## Description:

Baidu Web Search uses the SkillBoss API Hub to run real-time web searches and return structured results for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve current web results for fact-checking, latest-news questions, and queries about events, people, products, or places that need live verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to SkillBoss/HeyBossAI with the configured API key.

Mitigation: Install only when that external query handling is acceptable, prefer platform-managed SKILLBOSS_API_KEY, and avoid committing local credential files.

Risk: The documented shell invocation can expose users to command-injection risk if raw user input is interpolated into a shell command.

Mitigation: Invoke the search script with an argument-array execution path and validate the result count instead of constructing shell strings from user text.

Risk: Dependency and local installation handling need review before use.

Mitigation: Pin dependencies, add a lockfile, and verify credential-file ignore rules before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-baidu-web-search)

## Skill Output:

**Output Type(s):** [json, text, guidance]

**Output Format:** [JSON search results for agent use, with downstream answers typically written as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count defaults to 20 and is capped at 50; results include title, URL, snippet, total, query, and engine fields.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
