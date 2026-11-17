## Description:

Collects articles from configured WeChat public accounts for a requested date range, reads available mirrored or official sources, and organizes the results into a concise topic-based digest with source attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinntrance](https://clawhub.ai/user/jinntrance)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to summarize recent WeChat public-account articles across a configured account list, group the findings by topic, and assess which accounts provided useful signal during the requested period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a configured public-account list and saves a local digest in Documents.

Mitigation: Use it only with account lists and local output paths you are comfortable exposing to the agent.

Risk: Broad article-summary requests could unintentionally trigger the WeChat digest workflow.

Mitigation: Confirm that the requested task is specifically a WeChat or public-account digest before running it.

Risk: Public article sources may be unavailable, require login, return imprecise dates, or trigger anti-bot checks.

Mitigation: Prefer mirrored or official sources, mark unavailable accounts in the digest, and stop for human intervention when access controls or verification challenges appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinntrance/skills/ai-info-digest)
- [ClawHub publisher profile](https://clawhub.ai/user/jinntrance)
- [Skill instructions](artifact/SKILL.md)
- [WeChat account configuration](artifact/wechat-accounts.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown digest with source links, topic sections, and an account evaluation table; also saved as a local .md file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The digest is organized by theme, cites source accounts, and records accounts or sources that could not be fetched.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
