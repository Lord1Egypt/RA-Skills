## Description:

Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve CCTV Xinwen Lianbo items for a requested date and have an agent summarize the returned titles and article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can follow unvalidated article links from remote CCTV pages and may send a hardcoded cookie to unintended destinations.

Mitigation: Restrict article fetches and redirects to known CCTV hosts, and remove the hardcoded cookie unless it is strictly required.

Risk: Installing dependencies without the lockfile can introduce unreviewed package changes.

Mitigation: Install dependencies from the committed lockfile and review dependency changes before release.

Risk: Running the skill in sensitive environments could expose private network access through outbound fetch behavior.

Mitigation: Review the skill before installation in environments with private networks or sensitive internal services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/cctv-news-fetcher-litiao)
- [CCTV Xinwen Lianbo recent archive](https://tv.cctv.com/lm/xwlb/)
- [CCTV Xinwen Lianbo legacy archive](https://cctv.cntv.cn/lm/xinwenlianbo/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary derived from JSON crawler results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill runs a Node/Bun crawler for a YYYYMMDD date and summarizes fetched title and content fields.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
