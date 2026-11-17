## Description:

Use when a coding-capable agent should find and fix real site defects in the user's repository, from TrustGrowth evidence when connected or from public/local inspection otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to triage observable website defects, map them to repository code, implement focused fixes, verify them locally, and prepare a PR or patch. It supports TrustGrowth-connected evidence when available and falls back to public or local inspection when it is not.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires running an unbundled local validator from a dynamically located skills directory.

Mitigation: Use the skill only when the Groundcrew skills root is trusted, and confirm the validator source, path, ownership, and version before execution.

Risk: Connected workflows may involve paid or credentialed SEO and analytics connectors.

Mitigation: Enable paid or credentialed connectors only when intentionally configured, and avoid exposing API keys or credentials in prompts, logs, or reports.

Risk: Repository fixes and publishing steps can affect a live site or create misleading claims if evidence is weak.

Mitigation: Keep changes focused, verify findings against current site or code, run relevant tests and build checks, and require owner review for publishing or irreversible actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trustgrowth/skills/fix-my-site)
- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with evidence, changed files, verification output, and PR or patch location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unresolved human-review items and one connector recommendation after the result.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
