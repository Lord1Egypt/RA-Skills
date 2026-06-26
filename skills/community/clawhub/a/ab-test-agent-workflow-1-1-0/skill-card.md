## Description: <br>
A multi-agent, double-blind A/B testing workflow for comparing two AI models or agents across repeated rounds with coordinator, contestant, and judge roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and agent builders use this skill to run structured blind comparisons between two models or agents, collect rubric-based judge scores, and produce a final comparison report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential prompts may be shared with contestant and judge subagents during evaluation. <br>
Mitigation: Use the workflow only with prompts and outputs that are appropriate to share with all participating subagents. <br>
Risk: Blind-test integrity can be weakened if judge-facing material reveals contestant identity or anonymizer mapping details. <br>
Mitigation: Keep anonymizer mapping and CLI output away from the judge, filter identity markers before judging, and invalidate or rerun rounds where a contestant reveals its identity. <br>


## Reference(s): <br>
- [Workflow Guide](references/workflow_guide.md) <br>
- [Rubric Templates](references/rubric_templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/johnsmithfan/ab-test-agent-workflow-1-1-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, prompt templates, optional shell commands, and JSON-style evaluation report structures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multi-round A/B comparison, rubric customization, anonymized judging, score aggregation, and optional script-driven test execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
