## Description:

Queries recent foreign-trade news from AEP Gateway and returns AI-generated titles, summaries, publication dates, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[focus-aim](https://clawhub.ai/user/focus-aim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve recent foreign-trade news, import/export policy updates, and international trade information. It is not intended for domestic news, entertainment news, or real-time stock and currency market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill setup can ask the user to paste an AEP bearer token into the assistant conversation and stores it unencrypted in the skill directory.

Mitigation: Prefer a platform secret store or environment variable; rotate the token if it was shared in chat; keep local .env files out of version control.

Risk: The dependency declaration allows a range for requests rather than pinning an exact version.

Mitigation: Install dependencies in an isolated environment and pin versions before production deployment.

## Reference(s):

- [AEP credential setup guide](artifact/references/aep-setup.md)
- [ClawHub skill page](https://clawhub.ai/focus-aim/skills/aim-trade-news)
- [Publisher profile](https://clawhub.ai/user/focus-aim)
- [AEP credential portal](https://tools.mentarc.cn/aim-skills/)
- [AEP Gateway trending_hub API endpoint](https://aep.vemic.com/trending_hub/ai_collection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the script, typically rendered by the agent as Markdown news summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AEP_AUTHORIZATION; the days parameter is limited to 1, 2, or 3; the skill does not cache news locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
