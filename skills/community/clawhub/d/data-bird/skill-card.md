## Description: <br>
Lightweight data analysis agent for workspace tables and HTTP(S)-downloaded CSV/Excel files that generates ECharts charts and written conclusions from natural language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niu001007](https://clawhub.ai/user/niu001007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze CSV or Excel business data, generate chart-ready ECharts JSON, and produce concise Markdown, HTML, or PDF reports with insights and artifact links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download user-provided HTTP(S) URLs from the runtime machine, including local or private-network addresses. <br>
Mitigation: Use trusted local files or public HTTPS CSV/Excel links, and block localhost, private-network, and cloud-metadata endpoints before allowing downloads. <br>
Risk: Optional MySQL access could expose databases if enabled with broad credentials. <br>
Mitigation: Keep MySQL disabled by default, and only enable it with read-only, narrowly scoped credentials. <br>
Risk: Generated HTML reports load active chart content and may be shared outside the execution environment. <br>
Mitigation: Review generated HTML before opening or sharing it, and prefer Markdown or PDF output when active content is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/niu001007/data-bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON with ECharts options, insight objects, Markdown report text, and file artifact paths for generated HTML/PDF/chart outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces chart arrays, report_md/reportMd, summary metadata, and artifacts containing report and chart paths; default limits include 5 charts, 10 MB files, and 10,000 rows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
