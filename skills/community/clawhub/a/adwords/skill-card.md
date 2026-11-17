## Description:

Adwords helps agents produce marketing copy, including headline formulas, body copy, AIDA drafts, pain-point prompts, testimonials, landing-page copy, SEO tips, hooks, CTAs, outlines, schedules, and content ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing teams use Adwords to ask an agent for ad copy, landing-page copy, headline variants, pain-point exploration prompts, testimonials, CTAs, SEO tips, outlines, schedules, and repurposing ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided marketing plans, customer details, or unpublished campaign text may be written to a local history file by scripts/script.sh.

Mitigation: Avoid sensitive inputs, set ADWORDS_DIR to a controlled location with appropriate permissions, or delete the history log after use.

Risk: Generated marketing claims, testimonials, pricing, and social-proof copy may be inaccurate or misleading if used without review.

Mitigation: Review and substantiate claims, testimonials, pricing, and conversion language before publication.

## Reference(s):

- [Adwords on ClawHub](https://clawhub.ai/bytesagain-lab/skills/adwords)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text emitted to stdout, with shell command usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands accept user-provided topics or targets; scripts/script.sh may append command inputs to ADWORDS_DIR/history.log.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
