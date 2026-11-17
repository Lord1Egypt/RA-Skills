## Description:

Helps an agent edit, review, polish, proofread, and refresh existing marketing copy while preserving the original message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, founders, content teams, and agents use this skill to improve existing marketing copy through structured sweeps for clarity, tone, benefits, proof, specificity, emotional resonance, and conversion risk. It is also useful for refreshing outdated pages or posts when facts, positioning, SEO needs, or brand voice have changed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on casual editing or proofreading requests because its trigger phrases are broad.

Mitigation: Confirm the user is asking to improve existing copy and keep the response scoped to copy editing rather than writing new material from scratch.

Risk: The skill may read a local product-marketing context file to match brand voice and customer language.

Mitigation: Use that context only to guide edits, and avoid exposing sensitive brand or customer details unless the user explicitly asks for them.

Risk: Suggested edits could add unsupported or misleading claims to marketing copy.

Mitigation: Preserve the original intent, flag proof gaps, and require user-provided evidence for statistics, testimonials, guarantees, and performance claims.

## Reference(s):

- [Copy Editing Checklist](references/checklist.md)
- [Content Refresh Editing](references/content-refresh.md)
- [Plain English Alternatives](references/plain-english-alternatives.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with issue notes, suggested edits, rewritten copy, checklists, and optional scoring]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include iterative editing passes, proof-gap flags, questions for the user, and concise rewritten alternatives.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata.version is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
