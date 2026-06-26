## Description: <br>
Family Financial Planner helps agents collect household financial details, model major life decisions such as resignation, entrepreneurship, relocation, full-time caregiving, or gap years, and produce an interactive single-file HTML dashboard with runway, scenario, and risk summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ramos-dev](https://clawhub.ai/user/Ramos-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate household financial readiness for major life choices, especially resignation, entrepreneurship, career changes, caregiving, relocation, or gap years. It is tailored to China-focused household finance modeling with city-specific social insurance, housing fund, living-cost, tax, debt, inflation, and runway assumptions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboards can contain sensitive household income, asset, debt, tax, and family-structure information. <br>
Mitigation: Keep generated HTML files private, avoid unnecessary personal identifiers, and share outputs only with trusted recipients. <br>
Risk: Free-text values inserted into an HTML dashboard could create unsafe or malformed output if not handled carefully. <br>
Mitigation: Escape or sanitize user-provided free text before inserting it into the template. <br>
Risk: The dashboard template may load Google Fonts, which is unsuitable for users who require a fully offline financial document. <br>
Mitigation: Remove the Google Fonts link before generating or distributing an offline-only dashboard. <br>


## Reference(s): <br>
- [Financial Model Specification](artifact/references/financial-model-spec.md) <br>
- [City Profiles](artifact/references/city-profiles.md) <br>
- [Dashboard Template](artifact/assets/dashboard-template.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/Ramos-dev/family-financial-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Concise Markdown guidance plus generated single-file HTML dashboard code when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated dashboard may contain private household financial data and should be kept private.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
