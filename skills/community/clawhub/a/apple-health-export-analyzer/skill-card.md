## Description: <br>
Use the Health Data AI Analyzer Mac app read-only localhost API on macOS to generate a concise Apple Health daily brief and 3 practical suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krumjahn](https://clawhub.ai/user/krumjahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this macOS skill to summarize their own imported Apple Health data through the Health Data AI Analyzer Mac app's read-only localhost API. It supports daily health briefs, recent step and sleep comparisons, and practical non-medical suggestions when the user explicitly asks for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health metrics may appear in the assistant conversation when summarized. <br>
Mitigation: Use the skill only for health data the user is comfortable including in chat history, and summarize only the minimum data needed for the request. <br>
Risk: The skill depends on a localhost Mac app API as the source of truth. <br>
Mitigation: Install only when the user trusts the local Health Data AI Analyzer Mac app, and prefer the localhost API response over raw Apple Health export files. <br>
Risk: Health summaries could be mistaken for medical advice. <br>
Mitigation: Keep outputs non-medical, avoid diagnoses, and report absent or null metrics as insufficient data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krumjahn/apple-health-export-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown daily brief with status, changes, suggestions, and missing data sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise non-medical summary; missing health metrics are reported as insufficient data.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
