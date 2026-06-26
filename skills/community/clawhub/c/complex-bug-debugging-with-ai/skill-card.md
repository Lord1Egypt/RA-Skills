## Description: <br>
A disciplined seven-stage workflow for AI-assisted debugging of complex, intermittent, multi-system bugs, with gates for evidence gathering, boundary testing, human decision-making, validation, escalation, and post-fix knowledge capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate AI-assisted investigation of difficult bugs that have unclear symptoms, intermittent behavior, multiple services, or failed first-line fixes. It structures the session into evidence collection, boundary tests, option review, supervised execution, validation, and reusable debugging notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may request production-style access such as database, Kubernetes, SSH, or logs. <br>
Mitigation: Grant only scoped, temporary access needed for the specific debugging session, and require confirmation before commands or fixes with side effects. <br>
Risk: Debugging notes may capture sensitive operational details, logs, hostnames, customer data, or secrets. <br>
Mitigation: Redact secrets, tokens, customer data, internal service names, hostnames, and sensitive logs before writing or sharing BUGxx.md-style notes. <br>
Risk: The workflow may proceed toward fixes after diagnosis unless supervised. <br>
Mitigation: Keep a human decision gate before any fix, production command, or persistent file write. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/complex-bug-debugging-with-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured checklists, tables, prompts, and command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce debugging plans, staged questions, validation tables, risk comparisons, and BUGxx.md-style knowledge capture when the user confirms.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
