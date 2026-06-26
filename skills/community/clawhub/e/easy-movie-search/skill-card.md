## Description: <br>
搜索电视剧、动漫、电影的百度网盘和夸克网盘资源链接。当用户询问任何影视作品的网盘链接、资源、下载地址时使用此技能，包括但不限于"有XX的网盘链接吗"、"XX在哪里下载"、"找XX的资源"等问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SusanKerrbq](https://clawhub.ai/user/SusanKerrbq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to ask an agent for Baidu Netdisk and Quark cloud-drive resource links for movies, TV series, and anime by title. It is intended for media-link search workflows where returned third-party links are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return third-party cloud-drive download links for media without authorization safeguards. <br>
Mitigation: Use it only for content that is known to be authorized, public-domain, or otherwise lawful. <br>
Risk: Returned Baidu Netdisk and Quark links are unverified external content. <br>
Mitigation: Review links before opening or downloading, and handle downloaded files as untrusted content. <br>
Risk: The skill depends on a third-party API for search results. <br>
Mitigation: Expect availability, accuracy, and freshness to depend on that external service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SusanKerrbq/easy-movie-search) <br>
- [Movie resource API endpoint](https://meng-ge.top/api/movieData/getMoviesByType) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown text containing media titles, resource type labels, Baidu Netdisk links, Quark links, and update times] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on a third-party API and should be treated as unverified external links.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
