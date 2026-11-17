## Description:

Produce a durable onboarding artifact for a codebase by writing or refreshing ONBOARDING.md with a read-this-first summary, system overview, dependency map, startup flow, auth flow, and important files backed by file:line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to orient themselves in an unfamiliar or stale codebase and produce a durable onboarding document that explains the repository structure, startup path, authentication behavior, dependencies, and key files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated onboarding documents can expose private repository structure, implementation details, or sensitive context if shared outside the workspace.

Mitigation: Review ONBOARDING.md before distribution and use the optional ShareOnboardingGuide upload only when sharing the generated guide externally is acceptable.

Risk: An onboarding document can become misleading if repository files change after generation.

Mitigation: Re-run the skill after material codebase changes so the document is refreshed with current file:line citations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/codebase-explainer)
- [Publisher profile](https://clawhub.ai/user/dennisrongo)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown document with file:line citations and a concise chat summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or refreshes ONBOARDING.md; may optionally support sharing the generated guide when available and user-approved.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
