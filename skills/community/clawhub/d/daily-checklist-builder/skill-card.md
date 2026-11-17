## Description:

Builds an accessible daily opening, shift and closing checklist for US front-of-house teams, with sign-off lines and state items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US restaurant, retail, warehouse, and hotel shift leads use this skill to create accessible opening, mid-shift, closing, and sign-off checklists with state- or city-specific items.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Shared checklists could expose customer or payment details.

Mitigation: Keep customer names, phone numbers, order numbers, and payment card details off shared checklists; use counts or placeholders.

Risk: Local requirements vary, and checklist sign-off does not certify compliance.

Mitigation: Verify site-specific requirements with the applicable state, city, or health authority, and do not present the checklist as compliance certification.

Risk: The lint tool overwrites an existing lint-report.md in its output directory.

Mitigation: Choose a dedicated output directory before running the tool.

Risk: The optional Windows app is a separate download and was not assessed by the security verdict.

Mitigation: Make a separate trust decision before downloading or running it, and verify its published SHA-256 hash first.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/daily-checklist-builder)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [A daily checklist with opening, mid-shift, closing, and sign-off sections, plus supporting notes.]

**Output Parameters:** [Site type, opening and closing times, equipment, state or city, checklist tasks, and print preferences.]

**Other Properties Related to Output:** [Includes clear step rewrites, local items with sources to confirm, accessibility and print notes, and sign-off fields; it is not a compliance certification.]

## Skill Version(s):

1.0.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
