## Description: <br>
Output validation gates for AI agent systems that help prevent hallucinated data, leaked internal context, wrong formats, duplicate sends, post-compaction drift, and false delegated completions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to apply pre-ship validation gates to agent outputs before they reach humans, external channels, or code workflows. It is most useful for reviewing messages, technical deliverables, scheduled outputs, and delegated-work handoffs for completeness, format, leakage, and verification gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner describes this as a narrow advisory lint/review helper rather than a complete validation framework. <br>
Mitigation: Invoke it explicitly as a review aid, keep human review in the delivery path, and do not treat a passed checklist as proof that all output risks are eliminated. <br>
Risk: The included shell checker inspects provided files or stdin and may flag patterns without full business context. <br>
Mitigation: Review any BLOCK or FIX findings before acting on them, especially when content intentionally contains examples, internal terms, or test data. <br>


## Reference(s): <br>
- [Gate Detail Reference](references/gates-detail.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zurbrick/agent-qa-gates) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces checklist-style review guidance and optional gate-check diagnostics for supplied content or files.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
