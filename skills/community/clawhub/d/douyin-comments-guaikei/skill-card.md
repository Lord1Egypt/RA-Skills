## Description:

Searches public Douyin videos, creator profiles, trending lists, work details, and comments through GuaiKei, returning structured data for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content teams, marketers, and analysts use the skill to research public Douyin videos, creators, trends, and comments for topic planning, competitor review, audience feedback, and sentiment analysis. It requires a GuaiKei API token and sends submitted search terms, links, or IDs to that service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted keywords, Douyin links, or IDs are sent to the third-party GuaiKei service, and scanner inspection was incomplete.

Mitigation: Use only public material that is appropriate to share with the service; avoid private or sensitive inputs, and review the skill before using it for sensitive work.

Risk: The security evidence notes an account-search capability and does not establish that every component is safe.

Mitigation: Use account discovery only for appropriate public research, and review the results before acting on them.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/douyin-comments-guaikei)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [GuaiKei service and API access](https://www.guaikei.com)
- [Demand mining guidance](artifact/references/demand-mining.md)
- [Customer acquisition guidance](artifact/references/customer-acquisition.md)
- [Output contract](artifact/references/contract.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON response envelope; concise text or Markdown summaries for analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be arrays or objects depending on the selected Douyin query.]

## Skill Version(s):

1.5.0 (source: server release evidence, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
