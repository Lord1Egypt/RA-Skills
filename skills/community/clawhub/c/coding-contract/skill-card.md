## Description: <br>
Generate language-agnostic coding contracts from requirements, including interface signatures, behavioral constraints, and verification checklists rather than implementation code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dachunggan](https://clawhub.ai/user/dachunggan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn requirements or brainstorming documents into reusable implementation specifications. It is intended for workflows where one agent or reviewer writes a precise contract and another implementer writes the code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated specifications may be written to an unintended path or overwrite an existing file. <br>
Mitigation: Confirm the target output path before saving and check whether the destination file already exists. <br>
Risk: An incomplete or ambiguous requirement can produce a contract that misguides implementation. <br>
Mitigation: Clarify feature scope, constraints, and verification expectations before generating the final spec. <br>
Risk: A generated contract may be treated as implementation-ready without review. <br>
Mitigation: Review the generated interface signatures, constraint layer, and checklist before assigning implementation work. <br>


## Reference(s): <br>
- [Coding Contract ClawHub Release](https://clawhub.ai/dachunggan/coding-contract) <br>
- [Specification Output Template](references/spec-template.md) <br>
- [Constraint Patterns Reference](references/constraint-patterns.md) <br>
- [Good vs. Bad Specification Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown file named spec.md with interface signatures, constraint tables, and verification checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output path is docs/specs/YYYY-MM-DD-<feature-name>.md unless the user specifies another location; generated specifications avoid complete implementation code.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
