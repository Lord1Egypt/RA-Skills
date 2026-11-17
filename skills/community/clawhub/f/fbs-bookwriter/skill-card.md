## Description:

FBS-BookWriter helps agents run a long-form writing workflow for books, manuals, white papers, industry guides, and reports, using Node.js tools for intake, session recovery, staged quality checks, and Markdown or HTML delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duhongchao-fbsir](https://clawhub.ai/user/duhongchao-fbsir)

### License/Terms of Use:

MIT-0

## Use Case:

Authors, editors, and agent developers use this skill to structure and continue long-form manuscripts, manage book-root state, run staged quality gates, and prepare Markdown or HTML deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipped shell and Node.js workflows can create command-execution and supply-chain exposure.

Mitigation: Install only from a trusted publisher, pin the released version, use a lockfile, and review workflows before running them in a production environment.

Risk: Book-root operations may read or write local project state and recovery memory.

Mitigation: Use simple trusted book-root paths, confirm ambiguous roots before execution, and review local recovery files before sharing or archiving manuscripts.

Risk: Publishing workflows may be affected by untrusted environment variables.

Mitigation: Run publishing commands only in a controlled environment with reviewed environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duhongchao-fbsir/skills/fbs-bookwriter)
- [Publisher profile](https://clawhub.ai/user/duhongchao-fbsir)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw skills configuration](https://docs.openclaw.ai/tools/skills-config)
- [FBS-BookWriter homepage](https://fbs-bookwriter.u3w.com/)
- [Skill full specification](references/01-core/skill-full-spec.md)
- [Runtime mandatory contract](references/01-core/runtime-mandatory-contract.md)
- [Version baseline v2.1.2](docs/history/version-baseline-v2.1.2.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON status from scripts, and generated project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; may read and write local book-root state, recovery memory, quality reports, deliverables, and release artifacts.]

## Skill Version(s):

2.1.2 (source: server release evidence, package.json, CHANGELOG released 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
