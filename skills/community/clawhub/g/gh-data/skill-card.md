## Description: <br>
股海罗盘 helps agents analyze and screen A-share stocks using multi-source market data, quantitative signals, trend predictions, and generated reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinpy](https://clawhub.ai/user/sunbinpy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect A-share stock data, run quantitative analysis and stock-screening workflows, and produce charts or DOCX reports for informational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain HTTP API calls can expose stock queries and API keys in transit. <br>
Mitigation: Use the skill only with trusted networks and endpoints, and avoid sending sensitive keys where plaintext transit is unacceptable. <br>
Risk: API keys or generated identifiers are stored in plaintext under the user's home directory. <br>
Mitigation: Restrict local file access, rotate purchased keys if exposure is suspected, and avoid sharing generated report environments. <br>
Risk: Generated stock analysis may be misleading, including hard-coded or stale financial report text. <br>
Mitigation: Treat all investment analysis as informational only and verify report claims against trusted financial sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunbinpy/skills/gh-data) <br>
- [股海罗盘 service and API key page](https://www.oraskl.com/ghdata-admin) <br>
- [Default analysis API endpoint](http://api.topeasychina.com:15099/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown responses with Python snippets plus generated DOCX reports and PNG charts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts public stock-data providers and a configured analysis API; writes reports and charts to local paths.] <br>

## Skill Version(s): <br>
2.0.22 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
