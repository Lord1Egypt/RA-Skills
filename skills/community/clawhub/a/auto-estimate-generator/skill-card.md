## Description: <br>
Automatically generate estimates from QTO data by applying pricing rules to BIM quantities for cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction estimators, BIM teams, and project engineers use this skill to convert BIM quantity takeoff data into structured cost estimates, summaries by category, and lists of unmatched items that need manual pricing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Estimate exports use filesystem access and could overwrite an existing project file if the output path is chosen carelessly. <br>
Mitigation: Choose an explicit project output path and avoid filenames or folders where overwriting existing files would matter. <br>
Risk: Incomplete or incorrect pricing rules can produce inaccurate cost estimates or leave QTO items unmapped. <br>
Mitigation: Review unmatched items, verify pricing rules, and manually confirm estimates before using them for project decisions. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/auto-estimate-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown estimate tables, structured summaries, Python examples, configuration guidance, and optional Excel report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flags QTO items with no matching pricing rule for manual review.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
