## Description: <br>
Cavecrew helps an agent choose between compressed-output investigator, builder, and reviewer subagents for code navigation, small edits, and diff review while preserving main-thread context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use Cavecrew to delegate focused code navigation, small edits, and review tasks to terse subagents when preserving main session context is important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad delegation or context-saving trigger phrases could activate the skill when the user did not intend it. <br>
Mitigation: Prefer explicit invocation and review where any saved context is written or reused. <br>
Risk: Terse subagent output can be hard for humans to interpret directly. <br>
Mitigation: Paraphrase compact findings before presenting them to a human reader. <br>


## Reference(s): <br>
- [Cavecrew ClawHub release](https://clawhub.ai/seanford/cavecrew) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown guidance with compact subagent output contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Terse, file-path-first outputs for investigator, builder, and reviewer delegation patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
