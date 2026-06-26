## Description: <br>
Distill Skill Builder guides agents through a pipeline for turning official documentation into structured knowledge skills, including source analysis, crawling or distillation, organization, evaluation, and iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create, evaluate, and improve knowledge skills from documentation sources. It is intended to help agents produce skill files, reference material, evaluator runs, and iteration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes persistent cross-agent deployment and sync guidance that may copy files into multiple assistant directories. <br>
Mitigation: Review planned file destinations before use and remove sync steps that are not needed for the target environment. <br>
Risk: The skill can guide agents to patch the bundled evaluator, which may change scoring behavior for future skill reviews. <br>
Mitigation: Review evaluator changes as code changes, keep patches scoped, and rerun evaluation after modification. <br>
Risk: The skill includes crawling and anti-bot workflow guidance that can trigger network activity. <br>
Mitigation: Use only approved documentation sources, respect site terms, and disable crawling steps when offline distillation is sufficient. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yhongm/distill-skill-builder) <br>
- [Skill distillation workflow](references/distillation-workflow.md) <br>
- [Skill evaluator guide](references/evaluator-guide.md) <br>
- [Skill iteration guide](references/iteration-guide.md) <br>
- [Crawling guide](references/crawling-guide.md) <br>
- [Metadata specification](references/metadata-spec.md) <br>
- [Naming conventions](references/naming-conventions.md) <br>
- [Quality standards](references/quality-standards.md) <br>
- [Self-checklist](references/self-checklist.md) <br>
- [SKILL.md structure](references/skillmd-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or revise skill files, reference documents, evaluator commands, and configuration snippets when used by an agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
