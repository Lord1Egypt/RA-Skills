## Description: <br>
上市公司年报/研报自动抓取，覆盖巨潮资讯、东方财富等数据源，支持按公司代码、名称、年份或行业批量下载 PDF，并可解析 PDF 文本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill to retrieve public company annual, quarterly, and research report PDFs from supported Chinese financial disclosure sources and optionally extract financial text from downloaded PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk financial report downloads can trigger source-site rate limits or blocks. <br>
Mitigation: Keep downloads rate-limited, use the documented low concurrency and randomized delays, and avoid commercial redistribution of downloaded reports. <br>
Risk: Logged-in sources may require cookies or Playwright storage state that function like credentials. <br>
Mitigation: Store session files outside shared repositories, restrict file permissions, and delete or rotate them when they are no longer needed. <br>
Risk: Automated PDF parsing can miss, misread, or return incomplete financial fields. <br>
Mitigation: Treat extracted figures as draft analysis and verify important values against the original public PDF before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tuobadaidai/financial-report-fetcher) <br>
- [CNINFO announcement query API](http://www.cninfo.com.cn/new/hisAnnouncement/query) <br>
- [Eastmoney report list API](https://reportapi.eastmoney.com/report/list) <br>
- [SSE listed company announcements](http://www.sse.com.cn/disclosure/listedinfo/announcement/) <br>
- [SZSE announcement API](https://disc.szse.cn/api/disc/info/ann/twoCategory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with command examples, Python code paths, downloaded PDF files, and JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local downloads and metadata; keep bulk requests rate-limited and protect any optional login session files.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
