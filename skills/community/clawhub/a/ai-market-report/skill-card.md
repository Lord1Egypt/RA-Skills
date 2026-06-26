## Description: <br>
Generates AI companion software market research reports by collecting App Store and web-research data, then producing Markdown, HTML, and PDF report files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vae2024](https://clawhub.ai/user/vae2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, product teams, and agents use this skill to assemble recurring AI companion app market reports covering App Store signals, public web research, market sizing, product positioning, and strategy recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-research prompts are sent to Apple/Tavily and may expose sensitive strategy terms or private company names. <br>
Mitigation: Avoid confidential product strategy, private company names, or unreleased plans unless that data sharing is approved. <br>
Risk: Generated market data and citations come from public web-derived sources and may be outdated, incomplete, or inaccurate. <br>
Mitigation: Review generated sources before relying on the report, and keep unavailable metrics marked as not public rather than filling gaps with guesses. <br>
Risk: Generated HTML and PDF files may contain untrusted web-derived content. <br>
Mitigation: Treat generated report files as untrusted output and inspect them before redistribution or operational use. <br>
Risk: The skill writes report files under the OpenClaw workspace. <br>
Mitigation: Run it in an appropriate workspace and review created files before sharing or archiving them. <br>


## Reference(s): <br>
- [Data collection reference](references/data_collection.md) <br>
- [Report template](assets/report_template.html) <br>
- [Apple iTunes Search API sample query](https://itunes.apple.com/search?term=Character+AI&media=software&limit=1&country=US) <br>
- [ClawHub release page](https://clawhub.ai/vae2024/ai-market-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with rendered HTML and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped report files under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
