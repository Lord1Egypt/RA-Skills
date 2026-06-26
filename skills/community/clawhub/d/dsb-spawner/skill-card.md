## Description: <br>
Spawner helps agents delegate heavier file-editing, build, or long-running work to one scoped sub-agent with model routing and completion checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Spawner to delegate work that is too large for inline handling while keeping roles, context, exit criteria, and retries constrained. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegating work may send selected project context to external model providers. <br>
Mitigation: Keep task scope narrow and include only the files needed for the sub-agent task; avoid sensitive files unless they are necessary. <br>
Risk: A sub-agent may fail to produce the expected artifact or result. <br>
Mitigation: Define concrete exit criteria, verify the output exists, and retry inline or with a fallback when the artifact is missing. <br>
Risk: Broad delegation can consume context or create unnecessary long-running work. <br>
Mitigation: Use the skill only for work that is too heavy for inline execution and run one sub-agent at a time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/dsb-spawner) <br>
- [Publisher profile](https://clawhub.ai/user/dodge1218) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown instructions with a reusable task template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates one sub-agent at a time and expects verification of the stated exit artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
