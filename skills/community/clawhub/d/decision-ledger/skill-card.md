## Description:

Decision Ledger helps agents turn meeting notes, chats, or project materials into a reviewable ledger of decisions, owners, deadlines, assumptions, reversal conditions, and dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, project leads, and governance reviewers use this skill to extract confirmed decisions, open questions, owners, deadlines, assumptions, reversal conditions, and follow-up dependencies from meeting notes, chats, or project documents. It is intended for reviewable decision tracking, not for inventing decisions or replacing legal audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce incorrect or unsupported decision records if source notes are incomplete or ambiguous.

Mitigation: Use the output as a review draft, preserve explicit pending-confirmation items, and require human confirmation before acting on decisions or deadlines.

Risk: Meeting notes or project materials may contain personal, confidential, or sensitive business information.

Mitigation: Process only appropriate local inputs, redact sensitive content when needed, and avoid publishing or sending outputs without review.

Risk: The bundled script includes inactive generic audit helpers that are outside the core decision-ledger workflow.

Mitigation: Disclose this behavior to users and prefer a future release that removes or clearly documents those helper paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/decision-ledger)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Structured Markdown, with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are review drafts and checklists derived from user-provided local input; missing information is surfaced as items to confirm.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
