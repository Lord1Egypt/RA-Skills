## Description:

Reviews async and concurrency code for deadlocks, race conditions, missing cancellation, blocking calls in async contexts, and misused primitives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnguyen1996](https://clawhub.ai/user/lnguyen1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review async and concurrent code across common programming languages. It helps identify correctness, reliability, and resource-management issues and returns prioritized fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the skill asks the agent to retain and reuse review-derived pattern statistics without clear consent, scope, or deletion controls.

Mitigation: Run the skill with review-pattern tracking treated as session-local, or disable persistence; do not store private code, identifiers, filenames, or free-form findings across reviews.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnguyen1996/skills/async-concurrency-reviewer)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown review report with severity ratings and corrected code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes critical findings, warnings, suggestions, correct patterns, and a concise summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
