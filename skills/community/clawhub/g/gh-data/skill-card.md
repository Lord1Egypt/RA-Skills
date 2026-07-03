## Description: <br>
A China A-share stock analysis and screening skill that gathers public market data, requests quantitative analysis, forecasts trends, and can generate stock-analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinpy](https://clawhub.ai/user/sunbinpy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze China A-share stocks, screen candidate stocks, inspect technical and financial signals, and produce human-readable stock-analysis outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically creates and reuses a persistent local API key at ~/.ghdata/ghdataapikey. <br>
Mitigation: Disclose this persistence before use, document how to inspect or delete the file, and avoid exposing the key in logs or shared report artifacts. <br>
Risk: Stock queries, screening filters, and the API key may be sent to a remote analysis service. <br>
Mitigation: Use the skill only for queries the user is comfortable transmitting, and review the configured endpoint and network policy before deployment. <br>
Risk: Generated financial reports may include fixed or generic risk language rather than fully data-backed analysis. <br>
Mitigation: Treat outputs as decision support, require human review, and verify conclusions against source market data before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunbinpy/skills/gh-data) <br>
- [Publisher profile](https://clawhub.ai/user/sunbinpy) <br>
- [Project homepage](https://www.oraskl.com/ghdata-admin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, structured stock-analysis text, and optional DOCX/PNG report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local report files under the configured document directory and persist an API key file at ~/.ghdata/ghdataapikey.] <br>

## Skill Version(s): <br>
2.0.23 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
