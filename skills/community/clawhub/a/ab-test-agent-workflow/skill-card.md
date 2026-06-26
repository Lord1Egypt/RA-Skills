## Description: <br>
Coordinates a multi-round, double-blind A/B workflow for comparing AI models or agents with anonymized contestant outputs and judge scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and evaluators use this skill to compare two AI models or agents across repeated blind judging rounds. It helps collect contestant outputs, anonymize them for review, score them against a rubric, and summarize the final comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running multiple blind-test rounds can consume additional model or subagent calls. <br>
Mitigation: Set the number of rounds deliberately and monitor usage before running larger comparisons. <br>
Risk: Optional script-driven mode can fail if referenced script paths are not present in the installed artifact. <br>
Mitigation: Verify optional script paths exist before using script-driven mode, or use the pure AI coordination workflow. <br>
Risk: Contestant outputs may reveal model identity and weaken the blind comparison. <br>
Mitigation: Anonymize identity markers before judging and keep the judge prompt focused on source-hidden plan labels. <br>
Risk: Judge scores and comments may be subjective or misleading for high-stakes decisions. <br>
Mitigation: Review the rubric, outputs, scores, and final report before relying on the comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ab-test-agent-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, optional shell commands, and a structured JSON-style final report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use multiple model or subagent calls across configured evaluation rounds.] <br>

## Skill Version(s): <br>
1.1.0-en2 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
