## Description: <br>
像生命进化一样复制、变异、选择--让Skill在迭代中自我优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to iteratively improve agent skills by copying a baseline skill, creating variants, testing versions, and selecting a preferred result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled local script can copy and mutate skills with weak path controls. <br>
Mitigation: Use plain skill slugs rather than paths and inspect any files created under .memory/evolution before using or publishing them. <br>
Risk: The script reports simulated test scores and selected best versions that are not real quality evidence. <br>
Mitigation: Treat reported scores as placeholders and perform manual review, testing, and security scanning before adopting a selected variant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/apollo-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash command examples and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or modifies skill variant directories under .memory/evolution when the bundled script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
