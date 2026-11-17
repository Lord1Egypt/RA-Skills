## Description:

Provides A-share shareholder data lookups for top shareholders, top tradable shareholders, shareholder counts, shareholder holding changes, and equity pledge summaries or details using market.ft.tech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query current and historical A-share shareholder structure, holder-count changes, shareholder increase or decrease activity, and market or stock-level equity pledge information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock query parameters are sent to market.ft.tech.

Mitigation: Use only stock identifiers intended for that service and avoid submitting sensitive or private query context.

Risk: The dispatcher can be steered toward unintended local Python handler execution if the subskill argument is misused.

Mitigation: Restrict execution to the six documented subskill names and reject path traversal before broad deployment.

Risk: The release security verdict is suspicious due to dispatcher behavior, although no credential theft, persistence, or destructive behavior was found.

Mitigation: Review and scan the skill before deployment, then rerun security checks after fixing the dispatcher allowlist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-holder-data)
- [market.ft.tech API base](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries or tables derived from JSON API responses, with optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires stock codes with market suffixes such as SH, SZ, or BJ for stock-specific queries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
