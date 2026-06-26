## Description: <br>
Configurable quality evaluation for AI agent outputs, with criteria definition, pattern-based checks, manual scoring, trend tracking, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and agent teams use this skill to define rubrics, evaluate text outputs, compare prompt or model changes, and track quality trends over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved history and reports may contain private prompts, proprietary responses, personal data, or other sensitive agent outputs. <br>
Mitigation: Use trusted terminals and output directories, avoid scoring secret material when persistence is enabled, and protect or delete generated history and report files as needed. <br>
Risk: Automated scoring is pattern-based and may miss factual errors or produce false positives on surface-level checks. <br>
Mitigation: Use manual or blended scoring for high-impact evaluations and review scorecard results before making release or quality decisions. <br>


## Reference(s): <br>
- [Agent Scorecard on ClawHub](https://clawhub.ai/TheShadowRose/agent-scorecard) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated score reports may be Markdown or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with standard-library Python; stores optional JSONL history and report files when requested.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
