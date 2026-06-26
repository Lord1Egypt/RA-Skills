## Description: <br>
Conducts enterprise-grade research with multi-source synthesis, citation tracking, source credibility scoring, and verified citation-backed report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emiltsoi](https://clawhub.ai/user/emiltsoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill for complex research tasks such as comprehensive analysis, technology comparisons, state-of-the-art reviews, market analysis, and multi-perspective investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs autonomous web research and may verify citation URLs over the network. <br>
Mitigation: Use it only for research topics that are appropriate for network retrieval, and avoid confidential topics unless the workflow is changed to restrict or review outbound access. <br>
Risk: The skill writes research output and state in multiple local locations. <br>
Mitigation: Choose or review output locations before use, and remove retained citation or continuation state when the research is sensitive. <br>
Risk: The skill may spawn continuation agents for long reports. <br>
Mitigation: Require user confirmation before continuation agents are launched when controlling cost, scope, or data exposure matters. <br>
Risk: The skill auto-opens generated HTML/PDF output. <br>
Mitigation: Disable automatic opening or inspect generated HTML before viewing when working with untrusted or sensitive research content. <br>


## Reference(s): <br>
- [Deep Research Skill README](README.md) <br>
- [Deep Research Methodology](reference/methodology.md) <br>
- [Report Assembly](reference/report-assembly.md) <br>
- [Quality Gates](reference/quality-gates.md) <br>
- [HTML Generation](reference/html-generation.md) <br>
- [Auto-Continuation Protocol](reference/continuation.md) <br>
- [WeasyPrint Guidelines](reference/weasyprint_guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with citations, plus generated HTML/PDF files and JSON citation or continuation state when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under ~/Documents/[Topic]_Research_[Date]/; citation and continuation state may also be retained under ~/.claude/research_output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
