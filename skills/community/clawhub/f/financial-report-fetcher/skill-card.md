## Description:

Fetches public company annual reports and research reports from financial disclosure and market-data sources, with support for batch PDF downloads and optional PDF text extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial analysts use this skill to locate and download public annual, periodic, and research-report PDFs for listed companies by stock code, company name, year, or industry. Agents can also use it to parse downloaded PDFs for selected financial metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe download patterns may save untrusted PDF content from public financial sites.

Mitigation: Run the skill in an isolated virtual environment or container, keep downloads in a dedicated directory, and validate HTTPS, path handling, content type, file size, and PDF signatures before opening or processing files.

Risk: Session or login workflows can expose local authentication state if used with authenticated report platforms.

Mitigation: Avoid authenticated Hibor or login-based workflows unless session files are secured, excluded from source control, and run by a non-privileged user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/financial-report-fetcher)
- [CNINFO announcement query endpoint](http://www.cninfo.com.cn/new/hisAnnouncement/query)
- [Eastmoney report list endpoint](https://reportapi.eastmoney.com/report/list)
- [SSE disclosure query endpoint](http://query.sse.com.cn/sseQuery/commonQuery.do)
- [SZSE disclosure API endpoint](https://disc.szse.cn/api/disc/info/ann/twoCategory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files, JSON]

**Output Format:** [Markdown guidance with shell commands; downloaded PDF files, metadata JSON, and optional parsed text or financial-data summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network access to public financial data sources is required; downloaded PDFs should be treated as untrusted files until validated.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
