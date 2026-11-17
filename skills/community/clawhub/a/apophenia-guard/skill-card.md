## Description:

Apophenia Guard is a cognitive bias interceptor for debugging sessions that detects unsupported pattern-matching, red herrings, and confirmation bias before they steer an investigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill during debugging sessions to identify cognitive traps in their reasoning and receive concrete counter-actions such as inversion, control-case comparison, or restarting from the original symptom.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may flag a reasoning pattern as biased when the debugging evidence is still incomplete.

Mitigation: Treat interventions as prompts for review, then validate claims against observed logs, tests, and control cases before changing code.

## Reference(s):

- [Apophenia Guard on ClawHub](https://clawhub.ai/jcools1977/skills/apophenia-guard)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown intervention text with structured observations, trap labels, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API calls, code execution, local data access, settings persistence, or environment changes indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
