## Description:

Searches public Douyin videos, creator posts, comments, and trending topics, then returns structured data for content and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, ecommerce teams, and marketers can search public Douyin content, inspect creator accounts and comments, and check trending topics to support content research, competitor analysis, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: 24 of 42 components were scanned and 18 were only partially inspected, so tool scope and runtime permissions were not verified.

Mitigation: Review the skill's permissions and inspect its components before installation or use; the scan does not establish malicious behavior but cannot rule out issues in content it could not fully interpret.

Risk: Search keywords and Douyin links are sent to the third-party API at guaikei.com, and requests require GUAIKEI_API_TOKEN.

Mitigation: Use only public content you are authorized to analyze, account for this data transfer, and keep the API token private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-traffics-monitor)
- [Usage options](artifact/references/options.md)
- [Comment demand analysis guide](artifact/references/demand-mining.md)
- [Changelog](artifact/references/changelog.md)
- [API access and support](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON records with agent-facing usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover public Douyin content; available fields and request limits depend on the API plan, and media links may expire.]

## Skill Version(s):

1.4.2 (source: release evidence, SKILL.md frontmatter, package.json, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
