## Description: <br>
Automates company due diligence by using Playwright-based browser workflows to query Chinese business, financial, and legal data sources and generate Markdown and PDF reports with screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guangningsun](https://clawhub.ai/user/guangningsun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and diligence teams use this skill to collect public company records, financial market data, litigation signals, screenshots, and source summaries for preliminary company due diligence reports. <br>

### Deployment Geography for Use: <br>
Global; practical coverage is focused on Chinese companies and Chinese public or commercial data sources. <br>

## Known Risks and Mitigations: <br>
Risk: Bundled session files may contain exposed authentication tokens. <br>
Mitigation: Remove bundled session files before installation and create fresh sessions outside the skill directory with restrictive file permissions. <br>
Risk: Unsafe shell command construction can allow command injection when company names, paths, or agent-supplied inputs are untrusted. <br>
Mitigation: Review and replace shell-string invocations with argument-list subprocess calls or strict input quoting before using untrusted inputs. <br>
Risk: Company names, screenshots, and browsing activity may be sent to third-party business, financial, and legal data services. <br>
Mitigation: Use approved accounts and avoid confidential targets unless this data sharing is acceptable for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guangningsun/company-due-diligence) <br>
- [Data sources reference](artifact/references/data_sources.md) <br>
- [Due diligence framework](artifact/references/framework.md) <br>
- [Report template](artifact/assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, PDF reports, screenshots, JSON data files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on third-party site availability, account access, saved browser sessions, and optional PDF tooling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact documentation also mentions internal version 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
