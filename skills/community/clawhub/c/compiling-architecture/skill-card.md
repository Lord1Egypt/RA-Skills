## Description: <br>
Guides agents through deterministic architecture pattern selection, spec compilation, constraint and NFR iteration, decision auditing, and final architecture approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inetgas](https://clawhub.ai/user/inetgas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn known project constraints, NFRs, and provider choices into reproducible architecture artifacts and reviewable pattern decisions before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward compiler registry maintenance even though the security review notes under-scoped authority around architecture vocabulary changes. <br>
Mitigation: Require explicit human approval before any change under schemas/, especially capability-vocabulary.yaml, and review the separate architecture compiler repository before allowing its Python tools to run. <br>
Risk: Architecture outputs may be treated as approved even when provider, runtime, auth, storage, retention, or messaging choices remain unresolved. <br>
Mitigation: Use the provider-binding gate and require fresh review after provider choices, brownfield discoveries, or architecture drift change the approved spec. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inetgas/compiling-architecture) <br>
- [Architecture compiler homepage](https://github.com/inetgas/arch-compiler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML artifacts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce architecture spec files, compiled pattern summaries, review prompts, and approval guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
