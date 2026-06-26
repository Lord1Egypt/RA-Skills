## Description: <br>
Generate structured competitive analysis reports with feature comparisons, pricing analysis, SWOT, and strategic recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, marketing, product, and strategy teams use this skill to research public competitor information and produce client-ready competitive intelligence reports with feature, pricing, SWOT, positioning, and recommendation sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill researches public competitor information and may produce inaccurate or outdated market claims if source data is stale. <br>
Mitigation: Review cited public sources, pricing, and assumptions before using the report for business decisions. <br>
Risk: Generated reports may overwrite or add files under output/competitor-analysis/. <br>
Mitigation: Check the output directory before rerunning when existing reports or sensitive business context matter. <br>
Risk: The skill can propose shell commands through its allowed tool surface. <br>
Mitigation: Review any proposed shell command before allowing execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/delonix-competitor-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Files] <br>
**Output Format:** [Markdown, HTML, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves a full report, styled HTML version, executive summary, and feature matrix under output/competitor-analysis/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
