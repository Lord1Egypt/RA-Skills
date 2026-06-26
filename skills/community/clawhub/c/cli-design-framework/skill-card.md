## Description: <br>
Use when designing a new CLI, reviewing an existing CLI, or resolving uncertainty about a CLI's role, user type, interaction form, statefulness, risk profile, or human-vs-machine surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wangnov](https://clawhub.ai/user/Wangnov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CLI maintainers use this skill to classify, design, or review command-line interfaces before deciding command shape, output contracts, state model, and safety guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides design guidance, and its example runtime blueprint discusses approvals, local state, transcript retention, and secret handling that may be implemented incorrectly if copied as production architecture. <br>
Mitigation: Use the examples as starting points only; add project-specific safeguards for approvals, storage, transcript retention, and secret handling before implementing those ideas. <br>
Risk: Incorrect CLI classification can lead to mismatched human, automation, state, or safety surfaces. <br>
Mitigation: Review the classification and derived design consequences against the actual CLI audience, side effects, and state model before adopting the recommendations. <br>


## Reference(s): <br>
- [CLI Design Framework Skill](SKILL.md) <br>
- [Taxonomy](references/taxonomy.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Classification Examples](references/classification-examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Wangnov/cli-design-framework) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prose with structured classification, design blueprint, or review sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concrete command-shape guidance, output-contract recommendations, risk ladders, and unresolved classification questions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
