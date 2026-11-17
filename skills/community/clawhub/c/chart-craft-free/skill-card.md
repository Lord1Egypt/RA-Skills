## Description: <br>
Chart Craft Free helps agents create basic local charts with Python and matplotlib, including bar, line, pie, and scatter charts plus chart-type recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and reporting users can use this skill to turn small structured datasets into local PNG charts and receive basic guidance on which chart type fits the data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores chart data, generated images, and chart history on the local filesystem. <br>
Mitigation: Avoid highly sensitive datasets unless local retention is acceptable, and review permissions on the chart output directory. <br>
Risk: The documentation mixes no-network claims with references to LLM API and callback_url fields. <br>
Mitigation: Clarify the intended networking model before using callback URLs or external agent integrations. <br>


## Reference(s): <br>
- [Chart Craft Free on ClawHub](https://clawhub.ai/thcjp/skills/chart-craft-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Configuration instructions] <br>
**Output Format:** [Markdown guidance with bash commands, local PNG chart files, and chart metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes chart history and generated chart images to a local user-directory path when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
