## Description:

A tool to query Chinese listed company announcements from SZSE (Shenzhen Stock Exchange) and SSE (Shanghai Stock Exchange), including single or batch stock queries, keyword searches, and date-range filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noahstepheno](https://clawhub.ai/user/noahstepheno)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to retrieve A-share listed-company announcements from SZSE and SSE by stock code, keyword, and date range. It can be used directly as a Python script or integrated into an OpenClaw workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Announcement searches are sent over unencrypted HTTP.

Mitigation: Use only where outbound requests to SZSE and SSE are acceptable, avoid sensitive search terms, and independently verify announcements before relying on them for financial decisions.

Risk: Dependencies are loosely constrained.

Mitigation: Pin dependencies and remove the unused openclaw requirement before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noahstepheno/skills/cn-stock-announcements)
- [Publisher profile](https://clawhub.ai/user/noahstepheno)
- [SZSE announcement API endpoint](http://www.szse.cn/api/disc/announcement/annList?random=)
- [SSE latest bulletin API endpoint](http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-formatted announcement results with inline links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns separate SZSE and SSE result lists; each item includes stock identifiers, announcement title, publication date or time when available, and a source link.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
