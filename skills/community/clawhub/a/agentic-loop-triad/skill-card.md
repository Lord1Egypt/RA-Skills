## Description: <br>
Unifies intent engineering, execution, and feedback into an autonomous loop that detects drift, learns patterns, revises specifications, transfers prior goal knowledge, and produces verifiable improvement records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run a local self-improvement pipeline from a goal or existing specification through analysis, revision, state tracking, and improvement reporting. It is suited for workflows that need repeatable audit files and human review points around automated changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local pipeline writes audit and state files and can auto-revise targets across runs. <br>
Mitigation: Use a dedicated output directory, review revision_rationale.md and revised_specification.json before accepting changed targets, and run with --no-auto-revise or --no-transfer when stricter human control is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielfoojunwei/agentic-loop-triad) <br>
- [Integration Guide](artifact/references/integration_guide.md) <br>
- [Paradigm Shifts Reference](artifact/references/paradigm_shifts_reference.md) <br>
- [Pipeline Configuration](artifact/references/pipeline_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSON and Markdown audit, state, specification, analysis, and improvement files in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
