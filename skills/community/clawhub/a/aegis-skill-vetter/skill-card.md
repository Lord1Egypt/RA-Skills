## Description: <br>
Enterprise-grade security vetting protocol for AI agent skills with automated threat detection, quantified risk scoring, and zero-trust code analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r00tFe1](https://clawhub.ai/user/r00tFe1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to review third-party agent skills before installation, applying source, code, permissions, dependency, and behavior checks to produce a risk-informed install decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security scoring may be over-trusted as an install or rejection authority. <br>
Mitigation: Use the skill as a review aid and require human confirmation for high-impact install or rejection decisions. <br>
Risk: Command examples could be run outside the intended candidate skill directory. <br>
Mitigation: Review command snippets before running them and keep scans scoped to the candidate skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/r00tFe1/aegis-skill-vetter) <br>
- [Publisher profile](https://clawhub.ai/user/r00tFe1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with checklists, command examples, scoring tables, and audit report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory security review outputs; evidence.security says its scoring should not be treated as final authority.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
