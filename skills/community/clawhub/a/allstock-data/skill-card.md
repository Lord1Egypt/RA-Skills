## Description: <br>
allstock-data helps agents query stock data for China A-shares, Hong Kong, and US markets through Tencent Finance HTTP APIs by default, with optional adata SDK workflows for broader A-share data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HackSing](https://clawhub.ai/user/HackSing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to look up real-time quotes, historical K-line data, batch market data, and order book signals for China A-share, Hong Kong, and US equities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock symbols may be sent to external finance data providers. <br>
Mitigation: Use validated public stock-code inputs and avoid submitting confidential portfolio, strategy, or client information. <br>
Risk: Default quote lookups use plain HTTP and unauthenticated responses. <br>
Mitigation: Treat returned data as public and untrusted, prefer HTTPS endpoints where available, and verify important market data with trusted sources before acting. <br>
Risk: Optional adata SDK and proxy setup can introduce package and network trust exposure. <br>
Mitigation: Install adata only from trusted package sources, verify the package before use, and use only trusted proxies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HackSing/allstock-data) <br>
- [Tencent Finance quote endpoint](http://qt.gtimg.cn/q=sh600519) <br>
- [Tencent Finance K-line endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, Python snippets, endpoint patterns, and response-field mappings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock symbols, HTTP endpoint examples, response decoding notes, rate guidance, and optional adata SDK setup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
