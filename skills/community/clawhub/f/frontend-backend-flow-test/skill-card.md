## Description:

Audits frontend API calls against backend endpoint contracts to surface method, path, query, body, auth, and response mismatches before release or regression review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlawnsdk](https://clawhub.ai/user/dlawnsdk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare frontend request behavior with backend API contracts before releases, refactors, and regression review. It is best suited for static contract audits and narrow dev/staging follow-up checks when static evidence is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional live helper generator can unexpectedly change data.

Mitigation: Use the static audit workflow first and avoid generated live helpers unless the target is a safe dev/staging environment.

Risk: Generated helpers may persist or expose reusable credentials.

Mitigation: Do not use real reusable credentials; use disposable test credentials only after reviewing the generated files.

Risk: Known read-only delete path, credential handling, and template injection issues are unresolved in the optional live helper path.

Mitigation: Avoid scripts/generate_tests.py until those issues are fixed, and review any generated helper before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlawnsdk/skills/frontend-backend-flow-test)
- [Audit Scope](references/AUDIT-SCOPE.md)
- [Limitations](references/LIMITATIONS.md)
- [Audit Examples](references/EXAMPLES.md)
- [Live Mode](references/LIVE-MODE.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON audit reports, with optional generated Python helper files and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static audit is the primary output path; live helpers are secondary and should be limited to safe dev/staging validation.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
