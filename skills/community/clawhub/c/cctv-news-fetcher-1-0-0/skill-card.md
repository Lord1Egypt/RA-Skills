## Description: <br>
Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pppig1357](https://clawhub.ai/user/pppig1357) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve CCTV News Broadcast highlights for a requested date and summarize the returned items. It is intended for date-specific news lookup workflows that can run a local JavaScript crawler. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local JavaScript crawler that makes outbound requests to CCTV/CNTV pages. <br>
Mitigation: Install and run it only in environments where those outbound requests are acceptable. <br>
Risk: The crawler includes a static Cookie header in outbound requests. <br>
Mitigation: Review or remove the static Cookie header before use if cleaner outbound request behavior is required. <br>
Risk: Fetched news content depends on external page availability and parsing behavior. <br>
Mitigation: Review the summarized output for completeness and accuracy before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pppig1357/cctv-news-fetcher-1-0-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pppig1357) <br>
- [CCTV News Broadcast source pages](https://tv.cctv.com/lm/xwlb/day/) <br>
- [CCTV CNTV archive source pages](https://cctv.cntv.cn/lm/xinwenlianbo/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary based on JSON crawler output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Crawler output contains date, title, and content fields for each news item when source pages are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
