## Description: <br>
Multi-model council review that spawns 3-5 independent AI reviewers and applies mechanical synthesis so votes decide the final verdict, not orchestrator opinion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to obtain structured multi-model review for code, plans, architecture, and high-risk technical decisions before merge, deployment, or commitment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review inputs may be processed by multiple external model providers, exposing secrets, regulated data, private customer data, or proprietary code. <br>
Mitigation: Use only approved providers and data classes, redact sensitive inputs before review, and prefer a local or single-provider mode when provider exposure is not acceptable. <br>


## Reference(s): <br>
- [Council v2 ClawHub listing](https://clawhub.ai/zurbrick/council-v2) <br>
- [Review Types](references/review-types.md) <br>
- [Role Prompts](references/role-prompts.md) <br>
- [JSON Schemas](references/schema.md) <br>
- [Synthesis Rules](references/synthesis-rules.md) <br>
- [OpenClaw model docs](https://docs.openclaw.ai/concepts/models) <br>
- [OpenRouter](https://openrouter.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown instructions, shell command examples, and structured JSON review and synthesis outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviewer outputs are expected to follow the skill's JSON schema; synthesis includes vote-driven results, critical blocks, conditions, minority report, and exit codes.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
