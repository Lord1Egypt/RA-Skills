## Description:

Drafts a single email creative with subject-line variants, preheader, body copy, one primary CTA, plain-text alternate, and message-match notes tied to the destination page and approved claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and agents use this skill to draft or iterate one email creative for promotional, cold-outbound, or newsletter workflows. It helps keep copy aligned to the destination page, approved claim wording, and a follow-on testing or audit handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted email copy can include unsupported marketing claims when approved claim data or destination evidence is missing.

Mitigation: Keep unresolved claims visibly marked, require claim and destination review before sending, and use the separate audit workflow for scoring or veto decisions.

Risk: Campaign inputs, consent state, or personalization signals may include sensitive customer or recipient context.

Mitigation: Provide only the materials needed for the drafting task and review saved drafts or proposed claim events before reusing them elsewhere.

Risk: The skill produces creative drafts but does not perform email sending or suppression checks.

Mitigation: Require separate send approval and replay-safe consent or suppression verification before any campaign is sent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/email-creative-builder)
- [Source Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Email Creative Modes](references/email-creative-modes.md)
- [Subject Line Specs](references/subject-line-specs.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown email draft with labeled subject-line variants, preheader, body copy, CTA, plain-text alternate, claim notes, and handoff summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not send email, score email quality, rank subject lines, or run suppression checks; unresolved claims remain visibly flagged for review.]

## Skill Version(s):

19.0.0 (source: server release evidence, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
