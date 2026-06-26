## Description: <br>
Analyzes Hong Kong, US, and A-share stocks using quote data, technical indicators, financial ratios, multi-source news, and a seven-section report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate structured stock-analysis reports for HK, US, and A-share symbols. The reports combine market data, technical indicators, financial-ratio analysis, news sentiment, and operational guidance for further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded API credentials may be exposed or reused outside the publisher's intended environment. <br>
Mitigation: Remove or rotate embedded tokens before distribution or use, and load required credentials from environment variables or a managed secret store. <br>
Risk: Generated investment recommendations may be unreliable when simulated indicators or placeholder financial data are presented as analysis. <br>
Mitigation: Clearly label simulated or placeholder data, verify results against authoritative market data, and require qualified human review before acting on recommendations. <br>
Risk: Stock symbols and request metadata may be sent to third-party financial or news services. <br>
Mitigation: Disclose external data providers, verify their terms and privacy practices, and avoid sending sensitive user information with stock-analysis requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gaoren36-arch/gaoren-stock-analyst) <br>
- [Publisher Profile](https://clawhub.ai/user/gaoren36-arch) <br>
- [README](artifact/README.md) <br>
- [README_EN](artifact/README_EN.md) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/) <br>
- [Finnhub API](https://finnhub.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain-text stock-analysis reports with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call third-party financial and news services; some indicators and financial fields may be simulated or placeholders and should not be treated as investment advice.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
