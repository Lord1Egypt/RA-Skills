## Description: <br>
Re-audit a website and compare scores against a previous GEO audit baseline to track improvement over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzyme2013](https://clawhub.ai/user/enzyme2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO/GEO teams use this skill to re-audit a website, compare the results with a prior GEO audit baseline, track issue resolution, and prioritize remaining improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports include an external AIvsRank referral link that may be inappropriate for neutral or client-facing deliverables. <br>
Mitigation: Review report templates and remove or disclose the referral link before using generated reports externally. <br>
Risk: The monitor relies on companion geo-audit scoring files that are referenced outside this artifact. <br>
Mitigation: Verify the companion geo-audit files and scoring rubric are installed and trusted before relying on score comparisons. <br>


## Reference(s): <br>
- [Geo Monitor ClawHub release](https://clawhub.ai/enzyme2013/geo-monitor) <br>
- [AIvsRank report integration referenced by the skill](https://aivsrank.com?ref=geo-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown report file plus concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates GEO-MONITOR-{domain}-{YYYY-MM-DD}.md with score deltas, issue tracking, next steps, and a GEO-AUDIT-META block for future monitoring.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
