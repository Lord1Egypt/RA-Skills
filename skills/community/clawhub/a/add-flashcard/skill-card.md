## Description: <br>
Spaced repetition flashcard system <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to trigger a spaced repetition flashcard workflow from natural-language flashcard requests, including English and Chinese trigger phrases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate local capability_executor.py implementation that is not bundled with the artifact. <br>
Mitigation: Review the local executor before deployment, including what flashcard data it stores and any failure-reporting paths it uses. <br>
Risk: Broad English and Chinese trigger phrases could activate the flashcard workflow unintentionally. <br>
Mitigation: Narrow or confirm triggers in environments where accidental flashcard creation would be disruptive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/534422530/add-flashcard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline Python usage example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; execution depends on a local capability executor not included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
