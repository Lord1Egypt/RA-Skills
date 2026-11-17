## Description:

Multi-model council review that spawns 3-5 independent AI reviewers and applies mechanical synthesis so votes decide the final verdict rather than orchestrator opinion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Council v2 to get independent model reviews of code, plans, architectures, and multi-option decisions before merge, deployment, or other high-impact commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON mode can execute crafted Python code when untrusted input is serialized into the generated orchestration payload.

Mitigation: Do not use `--format json` with untrusted input until heredoc serialization is fixed; use text mode or trusted, reviewed inputs only.

Risk: Review content may be sent to multiple external model providers, which can expose secrets, proprietary code, customer data, or security-sensitive plans.

Mitigation: Submit only data approved for every configured provider, redact sensitive material, and run reviewer sessions with minimal read-only context.

Risk: Reviewer JSON and synthesis results can be malformed or misleading if trusted without validation.

Mitigation: Require strict reviewer JSON validation, inspect critical findings and minority reports, and re-run or substitute failing reviewers before relying on the synthesis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zurbrick/skills/council-v2)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw model docs](https://docs.openclaw.ai/concepts/models)
- [OpenRouter](https://openrouter.ai)
- [Review types](references/review-types.md)
- [Role prompts](references/role-prompts.md)
- [Council v2 JSON schemas](references/schema.md)
- [Mechanical synthesis rules](references/synthesis-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown orchestration prompts and JSON synthesis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewer orchestration prompts, structured synthesis with verdicts, critical blocks, minority reports, anti-consensus checks, and exit codes.]

## Skill Version(s):

2.0.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
