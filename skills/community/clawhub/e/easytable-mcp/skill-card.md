## Description:

Use when the user wants to check restaurant availability or make, change, or cancel a table reservation at a restaurant that books through easyTable booking widgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect easyTable restaurant availability and manage reservations through the user's own browser session. It supports listing booking areas, dates, and times, then creating, modifying, finding, or cancelling bookings with confirmation gates for write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required browser extension can bridge into a live easyTable browser tab and handle personal reservation data.

Mitigation: Review the extension source, version, update channel, and browser permissions before installing, and use it only with the intended easyTable tab open.

Risk: Create, modify, and cancel actions can change real restaurant reservations.

Mitigation: Keep confirmation gates enabled and verify booking details carefully before rerunning a write action with confirmation.

Risk: A broad browser profile may expose unrelated sensitive sessions to extension risk.

Mitigation: Use a limited browser profile or tightly scoped host permissions when operating the extension.

## Reference(s):

- [fetchproxy browser extension](https://github.com/chrischall/fetchproxy)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/easytable-mcp)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown or plain text responses with reservation availability, dry-run previews, confirmation prompts, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions are confirmation-gated before create, modify, or cancel operations are applied.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
