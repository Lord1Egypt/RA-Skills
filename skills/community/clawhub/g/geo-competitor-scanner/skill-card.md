## Description: <br>
Analyze competitor GEO (Generative Engine Optimization) strategies by examining content structure, Schema markup, llms.txt, and AI citation signals to identify strategic gaps and opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, SEO, and content strategy teams use this skill to compare their brand with competitors across GEO infrastructure, content structure, entity signals, and citation-oriented content gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes HTTP requests to user-supplied brand and competitor domains, which may create traffic to third-party sites or conflict with site terms if overused. <br>
Mitigation: Use reasonable competitor lists, respect site terms and rate limits, and scan only domains intentionally provided for the task. <br>
Risk: Saved reports may contain competitive analysis or business-sensitive observations if written to an inappropriate path. <br>
Mitigation: Save reports only to a non-sensitive path selected for the task and review outputs before sharing them. <br>
Risk: The scanner depends on Python packages for HTTP requests and HTML parsing. <br>
Mitigation: Install dependencies from trusted package sources in an environment appropriate for the scan. <br>


## Reference(s): <br>
- [Scan Methodology](references/scan-methodology.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/geo-competitor-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report or console text with competitive matrices, dimension scores, and prioritized recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make user-directed HTTP requests to supplied brand and competitor domains and can save a report to a user-selected local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
