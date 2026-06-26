## Description: <br>
BaoStock helps agents retrieve free China A-share market data, including K-line history, financial indicators, trading calendars, industry classifications, and index constituents without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernelh](https://clawhub.ai/user/kernelh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external agent users use this skill to install BaoStock and query China A-share market data for screening, analysis, data export, and example backtesting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references external Python packages for market-data access. <br>
Mitigation: Use reviewed pinned versions of baostock and pandas, or install from a lockfile in sensitive and reproducible environments. <br>
Risk: Example analysis, backtesting, or trading outputs can be mistaken for financial advice. <br>
Mitigation: Treat outputs as data analysis only and require independent review before using them for investment decisions. <br>
Risk: External market-data queries can return empty, delayed, or unavailable results. <br>
Mitigation: Check BaoStock login status, handle empty DataFrames and API errors, and validate returned data before downstream use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kernelh/baostock-1-0-3) <br>
- [BaoStock homepage](https://www.baostock.com) <br>
- [BaoStock Python API documentation](http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes BaoStock API usage guidance, installation commands, and data-analysis workflow examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
