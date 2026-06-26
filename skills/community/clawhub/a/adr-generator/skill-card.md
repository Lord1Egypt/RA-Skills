## Description: <br>
Architecture Decision Record generator that analyzes codebases and documents technical decisions with context, alternatives, and consequences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to draft Architecture Decision Records from codebase analysis or project discussions, capturing context, alternatives, decisions, consequences, and references for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ADRs may include sensitive repository history, internal documentation, names, or business context. <br>
Mitigation: Review and redact ADRs before committing, publishing, or sharing them outside the intended audience. <br>
Risk: Generated decision records may overstate rationale when historical evidence is incomplete. <br>
Mitigation: Have project maintainers verify the context, alternatives, deciders, and consequences before accepting the ADR. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/charlie-morrison/adr-generator) <br>
- [Skill source: SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with ADR templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed ADR file paths, sequential numbering guidance, and review-ready decision records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
