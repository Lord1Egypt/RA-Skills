## Description:

Helps agents plan, draft, review, and hand off Claude-oriented email prompts and campaigns with critique loops and human approval gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to create and evaluate Claude-oriented email prompts, campaign drafts, rewrite instructions, critique rubrics, variant sets, and approval-ready copy packets while keeping live email actions behind explicit human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad email planning or improvement tasks, including work that could affect live email systems.

Mitigation: Use it for drafting and review support, and require explicit human approval before live sends, contact imports, DNS/authentication changes, suppression edits, or production automation changes.

Risk: Email copy can include unsupported claims, overpromising subject lines, unsafe personalization, or changes that need brand, legal, product, or deliverability review.

Mitigation: Trace claims to supplied source material, review subject and preview alignment with the body, validate personalization fallbacks, and route required human review before production use.

## Reference(s):

- [Claude Email Skill Operating Checklist](references/operating-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured plain text with prompts, drafts, rubrics, variant sets, and QA notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, DNS/authentication changes, suppression edits, or production automation changes.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
