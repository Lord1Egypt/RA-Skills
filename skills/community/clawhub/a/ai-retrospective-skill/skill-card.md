## Description: <br>
AI Collaboration Retrospective is a tool-agnostic post-session analysis framework that reviews AI-assisted coding conversations across eight dimensions to identify improvement opportunities and generate structured retrospective reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amoshc](https://clawhub.ai/user/amoshc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after AI-assisted coding sessions to review conversation history, identify inefficient collaboration patterns, and produce actionable retrospective reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can review the full current conversation, which may include secrets or private data. <br>
Mitigation: Use explicit invocation only, avoid running it in sessions containing secrets or private data, and review the generated retrospective before sharing it. <br>
Risk: The workflow may save reports or write persistent memory/config changes without a clear approval step. <br>
Mitigation: Override the workflow to ask before saving reports or writing memory or configuration changes. <br>


## Reference(s): <br>
- [Analysis Dimensions](references/analysis_dimensions.md) <br>
- [Retrospective Report Template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown retrospective report and in-conversation analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write session retrospective files and, when supported by the host agent, persistent memory or configuration updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
