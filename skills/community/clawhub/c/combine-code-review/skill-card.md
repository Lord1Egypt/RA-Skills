## Description: <br>
Reviews Combine framework code for memory leaks, operator misuse, and error handling. Use when reviewing code with import Combine, AnyPublisher, @Published, PassthroughSubject, or CurrentValueSubject. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Swift Combine code for subscription retention, retain-cycle, threading, publisher, operator, and error-handling issues. It guides agents to report reproducible findings with scope checks, retention evidence, capture-chain reasoning, and file or line references for high-severity issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence an agent to produce incorrect or misleading code review guidance. <br>
Mitigation: Review findings before applying changes, and require the skill's hard gates for scope, subscription retention, capture-chain evidence, UI scheduling, severity, and file or line references. <br>
Risk: Incomplete snippets can lead to overconfident memory-leak or subscription-retention claims. <br>
Mitigation: When surrounding storage or ownership is unclear, mark the issue unknown or verify and ask for the missing context instead of assuming safety or failure. <br>
Risk: The skill may be applied outside its intended Swift Combine scope. <br>
Mitigation: Confirm that reviewed files import Combine or use Combine APIs from the quick reference before reporting findings; otherwise stop as out of scope. <br>
Risk: Granting unnecessary runtime privileges would exceed the behavior evidenced for this release. <br>
Mitigation: Use the skill as text-only review guidance; it does not require credentials, command execution, or persistent access. <br>


## Reference(s): <br>
- [Combine Publishers](references/publishers.md) <br>
- [Combine Operators](references/operators.md) <br>
- [Combine Memory Management](references/memory.md) <br>
- [Combine Error Handling](references/error-handling.md) <br>
- [ClawHub Release Page](https://clawhub.ai/anderskev/combine-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown code review findings, questions, and checklist-backed guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No command execution, credential access, persistence, or destructive behavior indicated by security evidence.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
