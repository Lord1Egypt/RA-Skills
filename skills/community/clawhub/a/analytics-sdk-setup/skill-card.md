## Description:

Use this skill whenever a user wants a coding agent to audit, install, reconcile, align, or fix TikTok Pixel and/or Meta Pixel code in a real repo, especially for duplicate init, tracking drift, event mapping, consent/CSP/LDU/privacy gating, or unclear analytics ownership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peter-wf](https://clawhub.ai/user/peter-wf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit, install, compare, align, and repair TikTok Pixel and Meta Pixel integrations in real repositories. It helps classify whether to implement directly, plan first, or ask blocking questions before changing tracking, privacy, consent, CSP, LDU, or identifier behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or enabling the skill from a mutable or unreviewed source can expose users to unexpected instruction changes.

Mitigation: Use a reviewed local copy or pin the skills CLI and repository source to an immutable version, and prefer project-scoped installation.

Risk: Tracking changes can alter consent handling, CSP behavior, limited data use, or identifier collection.

Mitigation: Confirm consent handling, CSP changes, LDU requirements, and whether identifiers or Advanced Matching are explicitly approved before enabling or changing tracking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peter-wf/skills/analytics-sdk-setup)
- [README](README.md)
- [Canonical skill specification](SKILL.md)
- [Install and event details](references/install-and-events.md)
- [Privacy, CSP, and data handling](references/privacy-and-csp.md)
- [Evaluation prompts](evals/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, questions, plans, implementation summaries, and code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode-dependent output for questions-first, plan-first, or direct implementation workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
