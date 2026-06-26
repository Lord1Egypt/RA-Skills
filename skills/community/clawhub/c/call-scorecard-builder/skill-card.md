## Description: <br>
Generates call scorecard dimensions, observation points, examples, training suggestions, and review cadence templates for sales, support, or interview calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external teams use this skill to turn call goals, roles, and good or poor examples into reviewable scorecard Markdown for training quality checks, interview quality evaluation, and sales coaching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run python3 locally and write output files during scripted generation. <br>
Mitigation: Review the input and output paths before execution, prefer dry-run or direct text generation when file writes are not needed, and keep generated scorecards as reviewable drafts. <br>
Risk: Call materials may contain personal, customer, or sensitive business information. <br>
Mitigation: De-identify sensitive content before use and avoid treating a single recording or transcript as a final personnel or performance determination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/call-scorecard-builder) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Output specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown or JSON, with optional local file output when the Python helper script is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for scripted generation; otherwise the agent can produce reviewable text directly from the bundled template and specification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
