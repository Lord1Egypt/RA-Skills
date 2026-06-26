## Description: <br>
A tool to query Chinese listed company announcements from SZSE (Shenzhen Stock Exchange) and SSE (Shanghai Stock Exchange), with support for single or batch stock queries, keyword searches, and time-range filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoahStepheno](https://clawhub.ai/user/NoahStepheno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agent workflows use this skill to retrieve official A-share company announcements by stock code, keyword, and date range, then present exchange-specific results and disclosure links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external stock-market data services, so query terms and stock codes are sent outside the local environment. <br>
Mitigation: Avoid sensitive or proprietary keywords and confirm that external market-data lookups are acceptable for the user's workflow. <br>
Risk: One market-data request uses unencrypted HTTP, which could allow results or links to be intercepted or altered in transit. <br>
Mitigation: Verify important announcements independently against official exchange pages before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NoahStepheno/cn-stock-announcements) <br>
- [SZSE announcement API](http://www.szse.cn/api/disc/announcement/annList?random=) <br>
- [SSE bulletin query endpoint](http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Python dictionary of exchange-specific announcement strings, commonly summarized as Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include stock identifiers, announcement titles, publication dates when available, and official disclosure links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
