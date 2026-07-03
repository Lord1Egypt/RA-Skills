## Description: <br>
Map your career trajectory: skill gap analysis, role transitions, and personalized learning roadmaps based on market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and career-planning agents use this skill to analyze a professional profile, compare current skills with target-role demands, explore role transitions, and generate learning roadmaps or offer-comparison reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can execute unintended local code from a crafted target-role input. <br>
Mitigation: Review before installing or running the CLI; until fixed, only run it with profile values you typed yourself and avoid target-role strings from untrusted sources. <br>
Risk: Career, market, and salary guidance can be estimated when job-board data is unavailable or incomplete. <br>
Mitigation: Treat recommendations as planning support, cite or verify current market data, and avoid presenting outcomes such as offers, salary increases, or career satisfaction as guaranteed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/career-path-advisor) <br>
- [Role categories and transferable skill mappings](references/roles.json) <br>
- [Input schema](schemas/input.schema.json) <br>
- [Output schema](schemas/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown reports and tables, with optional JSON output for programmatic use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a career profile with current role, years of experience, and location; optional skills, target role, industry, education, and company tier refine the analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
