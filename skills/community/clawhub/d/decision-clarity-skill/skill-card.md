## Description: <br>
Helps agents clarify ambiguous decisions by exposing assumptions, reducing problems to facts and constraints, simplifying options, and ending with a recommendation or next step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanezzzz](https://clawhub.ai/user/shanezzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to guide agents through ambiguous startup, product, content, operations, strategy, personal, or reasoning-audit decisions and convert them into clearer recommendations, decision rules, or tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision-support outputs may be misleading when the user's facts, constraints, or evidence are incomplete. <br>
Mitigation: Treat recommendations as structured decision support and verify important facts, legal limits, financial assumptions, and operational constraints before acting. <br>
Risk: Simplification can remove necessary complexity if adequacy is not defined first. <br>
Mitigation: Use the skill's adequacy, hard-constraint, and anti-pattern checks before accepting a simpler option. <br>
Risk: The security guidance recommends trusted environments and review before running helper commands. <br>
Mitigation: Install only in trusted ClawHub or compatible agent environments and review any commands proposed by surrounding workflows before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shanezzzz/decision-clarity-skill) <br>
- [Business Reference](references/business.md) <br>
- [Product Reference](references/product.md) <br>
- [Content Reference](references/content.md) <br>
- [Operations Reference](references/operations.md) <br>
- [Trigger Questions](references/trigger-questions.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision analysis with concise recommendations, decision rules, tests, or next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the lightest useful structure for the user's decision problem.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
