## Description:

A read-only Douyin data skill for searching public videos, creators, posts, comments, and trending lists, with structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content strategists, marketers, and analysts can use the skill to research public Douyin videos, creators, comments, and trends for topic planning, competitor analysis, sentiment review, and demand discovery. Searches send the supplied keywords or links to the Guaikei service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or links, including sensitive ones, may be sent to the third-party Guaikei service.

Mitigation: Review the query and links before running the skill; avoid sending sensitive terms or URLs.

Risk: Parts of the code were only partially analyzed, so the security review is incomplete.

Mitigation: Review the skill and its dependencies before installation, and account for the incomplete analysis when deciding whether to use it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/douyin-fengxiang)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results, with concise summaries or tables derived from the results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect public Douyin data available at query time. Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; queries and links are sent to Guaikei.]

## Skill Version(s):

1.5.0 (source: ClawHub release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
