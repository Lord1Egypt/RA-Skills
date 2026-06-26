## Description: <br>
Patterns and techniques for evaluating and improving AI agent outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boleyn](https://clawhub.ai/user/boleyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design self-critique, evaluator-optimizer, rubric-based, and test-driven refinement workflows for AI agent outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Iterative evaluation and refinement loops can fail to converge or consume excessive resources. <br>
Mitigation: Set explicit iteration caps and add convergence checks before deploying these patterns. <br>
Risk: Generated code or tests produced during refinement may be incorrect or unsafe to run directly. <br>
Mitigation: Review generated code and execute tests or generated commands only inside a sandboxed environment. <br>
Risk: Evaluation logs may retain sensitive prompts, outputs, or task data. <br>
Mitigation: Avoid storing sensitive prompts or outputs in evaluation logs, or redact them before retention. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boleyn/agentic-eval) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with Python code examples and checklist snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only reference patterns; no executable installer, credential access, or hidden behavior found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
