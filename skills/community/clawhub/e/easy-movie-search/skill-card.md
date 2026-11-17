## Description:

搜索电视剧、动漫、电影的百度网盘和夸克网盘资源链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[susankerrbq](https://clawhub.ai/user/susankerrbq)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for Baidu Netdisk or Quark links for TV shows, anime, and movies. The skill extracts the requested title, queries the disclosed movie-resource API, and formats available results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested movie or show titles are sent to a disclosed third-party API.

Mitigation: Use the skill only when users are comfortable sharing those search terms with the external service.

Risk: Returned Baidu or Quark links may lead to external downloads with copyright, safety, or platform-rule implications.

Mitigation: Review links before opening or sharing them and follow applicable copyright and platform rules.

## Reference(s):

- [Movie Resource API](https://meng-ge.top/api/movieData/getMoviesByType)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown list with resource names, type labels, Baidu Netdisk links, Quark links, and update times]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external Baidu Netdisk and Quark links returned by the disclosed third-party API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
