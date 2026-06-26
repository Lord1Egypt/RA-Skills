## Description: <br>
Analyzes frontend page performance and produces a structured optimization report for slow pages, weak Lighthouse or Core Web Vitals results, slow first-screen rendering, janky interactions, large bundles, and render-blocking resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to evaluate a page URL, Lighthouse metrics, network waterfall, bundle analysis, or project files and produce a structured performance optimization report with evidence, inferred causes, prioritized fixes, and missing-data caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private project files, reports, URLs, or performance metrics may be shared with the agent while using this skill. <br>
Mitigation: Provide only inputs that are approved for agent access and omit sensitive project details when they are not needed for the audit. <br>
Risk: Optimization advice may be incomplete or misleading when measurements are missing or based only on screenshots, structure, waterfalls, or resource lists. <br>
Mitigation: Review recommendations before applying them and prefer measured Core Web Vitals, Lighthouse data, network waterfalls, and bundle analysis when available. <br>


## Reference(s): <br>
- [Performance Metrics](references/metrics.md) <br>
- [Diagnosis Rules](references/diagnosis-rules.md) <br>
- [Report Template](references/report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cnoder-wgh/frontend-performance-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured performance audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Distinguishes observed evidence from inferred conclusions and flags missing metrics when input is incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
