## Description: <br>
Use when evaluating, testing, and optimizing an agent architecture or multi-agent system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ada01325150-alt](https://clawhub.ai/user/ada01325150-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review agent and multi-agent system architecture, map failure modes, define system-level tests, and prioritize optimization work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture descriptions may include secrets or unnecessary private system details. <br>
Mitigation: Remove credentials, sensitive implementation details, and unrelated private data before sharing architecture inputs with the skill. <br>
Risk: The optional local renderer writes Markdown to a user-selected output path. <br>
Mitigation: Run the renderer only on JSON inputs and output paths that were intentionally selected. <br>


## Reference(s): <br>
- [Architecture Review Framework v1.0.0](references/architecture-review-framework-v1.0.0.md) <br>
- [Optimization Patterns v1.0.0](references/optimization-patterns-v1.0.0.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ada01325150-alt/agent-architecture-evaluator) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ada01325150-alt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown architecture review with optional JSON-to-Markdown rendering] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces named review sections: architecture inventory, failure mode map, architecture test plan, optimization roadmap, measurement plan, and architecture recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
