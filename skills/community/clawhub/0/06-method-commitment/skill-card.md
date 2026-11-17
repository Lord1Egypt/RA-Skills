## Description:

Use when the user has a selected Candidate Method, multiple Candidate Methods to merge, a user-authored rough method, or a reconstructed chat method and wants to converge on one human-owned method outcome before experiment design, research framing, or risk review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research engineers use this skill to converge a selected, merged, user-authored, or chat-reconstructed research method into one reviewed method outcome before experiment design, research framing, or risk review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create or update method-commitment files in an existing workspace.

Mitigation: Review the chosen workspace root before use and preserve existing user-edited artifacts when resuming a workflow.

Risk: A method status other than committed is not downstream-ready and could mislead later workflows if routed as final.

Mitigation: Route only committed outputs downstream; treat provisionally-committed, needs-redesign, and reject-current-method outputs as blocked or do-not-route states.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/06-method-commitment)
- [Server-resolved GitHub provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/06-method-commitment)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown workflow artifacts and human-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces status-aligned method commitment artifacts and a method commitment summary under the selected workspace root.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
