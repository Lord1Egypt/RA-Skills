## Description: <br>
Generates Chinese A-share market reports with index levels, percentage changes, advance/decline counts, and manually supplemented trading-volume data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts use this skill to fetch public Chinese A-share market indicators, generate daily Markdown and JSON reports, and add missing trading-volume values when automatic sources do not provide them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs public market-data lookups against iwencai.com, so query text can be sent to an external data source. <br>
Mitigation: Use only non-confidential market queries and avoid entering account details, proprietary research terms, or other sensitive identifiers. <br>
Risk: Reports and JSON data are stored locally, including in a Desktop report folder. <br>
Mitigation: Review generated files before sharing them and manage local file permissions according to the sensitivity of any manually entered data. <br>
Risk: Trading-volume values may require manual entry, which can make reports incomplete or inaccurate if values are omitted or entered incorrectly. <br>
Mitigation: Confirm manually supplied volume figures against a trusted market-data source before using reports for analysis or distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/cn-stock-volume) <br>
- [README.md](README.md) <br>
- [EXAMPLES.md](EXAMPLES.md) <br>
- [DESIGN.md](DESIGN.md) <br>
- [Tonghuashun iWenCai](https://www.iwencai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local report and data files, uses a 24-hour cache, and may require manual volume values.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
