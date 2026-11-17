## Description:

通用网页数据抓取工具，支持使用 CSS 选择器抓取链接、提取 HTML 表格数据，并导出 CSV 或 JSON 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxiangfacai](https://clawhub.ai/user/wuxiangfacai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect public web page links or table data for research, market monitoring, competitor tracking, and content aggregation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper can fetch any URL reachable from the host, including localhost, private network addresses, or cloud metadata endpoints.

Mitigation: Run it in a network-restricted environment and use URL allowlisting before production use.

Risk: Scraped data is saved locally and may include sensitive content if the target URL exposes it.

Mitigation: Use a dedicated working directory, review generated CSV or JSON files, and avoid scraping untrusted or sensitive internal pages.

Risk: The artifact documents dependency installation without pinned versions.

Mitigation: Pin and review requests and beautifulsoup4 versions before deploying in repeatable or production workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files, JSON, CSV]

**Output Format:** [Terminal text plus generated CSV or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scraper writes output.csv by default or output.json when JSON output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
