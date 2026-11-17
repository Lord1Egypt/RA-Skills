## Description:

Applies fixes from a prior review-llm-artifacts run, with safe/risky classification, and respects verify-llm-artifacts output when present to skip false positives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to apply fixes from review-llm-artifacts results while preserving a locked finding set, honoring optional verification status, and requiring confirmation for risky changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly rewrite repository files while applying fixes.

Mitigation: Use --dry-run first, require a clean working tree or backup stash, lock fixes to parsed review finding IDs, and inspect the final diff before accepting changes.

Risk: The skill may run local project tooling, including unpinned package tools.

Mitigation: Prefer pinned or local-only tooling and run the skill only in repositories where agent-executed local commands are acceptable.

Risk: JavaScript test failures may be hidden by the documented test command behavior.

Mitigation: Require real test failure reporting and treat non-zero test exits as failed verification before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/fix-llm-artifacts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code-editing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit repository files after required safety gates, locked finding checks, and approvals for risky fixes.]

## Skill Version(s):

1.1.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
