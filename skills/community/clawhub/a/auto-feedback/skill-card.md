## Description: <br>
A self-improving feedback loop skill that works fully standalone OR integrates with intent-engineering and dark-factory when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze execution logs, plain text observations, or related outcome reports, then generate performance analysis, prioritized improvements, regression tests, alignment checks, and signed improvement reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom suggestion rules can run arbitrary Python code. <br>
Mitigation: Use only trusted suggestion_rules.json files, or replace or sandbox the rule engine before using custom rules. <br>
Risk: Generated files can carry forward sensitive input data. <br>
Mitigation: Run the skill on non-sensitive, user-selected inputs and avoid logs or specifications that contain secrets, credentials, private prompts, or confidential business data. <br>
Risk: Generated observations and specifications may be reused in later work without review. <br>
Mitigation: Review generated observation, analysis, report, and specification files before reusing them. <br>


## Reference(s): <br>
- [Feedback-Loop-v2 ClawHub release](https://clawhub.ai/danielfoojunwei/auto-feedback) <br>
- [Operations Guide](references/operations_guide.md) <br>
- [Alignment Values](references/alignment_values.json) <br>
- [Scoring Weights](references/scoring_weights.json) <br>
- [Suggestion Rules](references/suggestion_rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON files and Markdown-formatted reports, with optional shell commands for running the workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces observation, analysis, improvement report, updated observation, and optional updated specification files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
