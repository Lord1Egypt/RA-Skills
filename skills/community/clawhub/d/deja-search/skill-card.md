## Description:

deja-search helps agents search a user's past AI coding sessions with the deja CLI to recover prior decisions, preferences, and solved issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vshulcz](https://clawhub.ai/user/vshulcz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use the skill to recall prior decisions and solved issues before editing, debugging, recommending tools or designs, and reporting work as ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm fallback is unpinned and may download and run an unreviewed package; the available scan evidence is incomplete.

Mitigation: Avoid installing until the package fallback is pinned to a reviewed version and its execution is disclosed. If installing, review prompts to update or synchronize rules; account for the two local paths unavailable to the scan.

## Reference(s):

- [deja-vu memory for OpenClaw](https://vshulcz.github.io/deja-vu/guide/memory-for-openclaw.html)
- [deja-search on ClawHub](https://clawhub.ai/vshulcz/skills/deja-search)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text recall results and session summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the user's local session history.]

## Skill Version(s):

0.24.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
