## Description: <br>
Helps agents design software architectures by selecting patterns, validating prototypes, running tests, and documenting decisions with evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nntrivi2001](https://clawhub.ai/user/nntrivi2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill for system design, API design, scaling decisions, and ADR preparation where recommendations should be backed by working prototypes, integration checks, load tests, and measurable evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or modify prototype code and propose validation commands. <br>
Mitigation: Review generated code and commands before execution, and run validation in a controlled development environment. <br>
Risk: Broad routing language could invoke the skill for architecture-adjacent requests. <br>
Mitigation: Narrow trigger wording or require explicit system design, API design, scaling, or ADR intent before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nntrivi2001/agent-architecture-designer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, validation reports, and ADR text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include runnable prototype code, Docker manifests, security scan notes, metrics, monitoring guidance, alerts, and runbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
