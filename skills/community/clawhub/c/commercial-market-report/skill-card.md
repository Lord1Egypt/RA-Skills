## Description: <br>
Guides agents through commercial complex market research and generates Word, HTML, and PPTX report deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxarch1980](https://clawhub.ai/user/dxarch1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate, retail planning, and commercial development teams use this skill to collect city-specific market data, analyze competition and consumer demand, build financial assumptions, and produce market research deliverables for commercial complex projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may send project names, locations, and market research terms to external search services. <br>
Mitigation: Use only approved project inputs, avoid confidential location details where possible, and confirm that external search use is acceptable before running the workflow. <br>
Risk: The workflow can rely on local API keys and browser context. <br>
Mitigation: Use scoped API keys, a dedicated browser profile, and a controlled output folder when collecting data and generating files. <br>
Risk: Financial, market, and consumer trend figures may be incomplete, stale, or estimated. <br>
Mitigation: Review all sources, assumptions, and generated figures before using the reports for investment, planning, or client-facing decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dxarch1980/commercial-market-report) <br>
- [Commercial market report skill](SKILL.md) <br>
- [Chapters guide](references/chapters.md) <br>
- [Data sources guide](references/data-sources.md) <br>
- [Report format guide](references/report-format.md) <br>
- [PPT format guide](references/ppt-format.md) <br>
- [Tavily search API](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Agent workflow guidance plus generated DOCX, HTML, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports include market analysis, charts, financial modeling, and source notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
