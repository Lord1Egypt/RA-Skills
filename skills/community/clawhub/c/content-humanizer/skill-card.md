## Description:

Transforms AI-generated content into genuinely human-sounding text when drafts feel robotic, use AI cliches, lack personality, or read generically, and is not intended for initial content creation or SEO optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and content teams use this skill to audit AI-sounding drafts, rewrite them with more natural rhythm and specificity, and apply a supplied brand voice. It is intended for improving existing content rather than creating first drafts or SEO optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may transform supplied drafts and optional brand-voice context, which can include sensitive unpublished marketing content.

Mitigation: Use appropriate input handling for confidential drafts and review the rewritten output before sharing or publishing.

Risk: Humanizing content can change tone, emphasis, or factual specificity in ways that misrepresent the intended message.

Mitigation: Compare the output against the original brief, supplied evidence, and brand voice before publication.

Risk: The skill documentation includes a fallback to Chinese when language detection fails, which may produce the wrong language for some drafts.

Mitigation: Specify the target language when the source content is short, mixed-language, or ambiguous.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/content-humanizer)
- [AI Tells Checklist](references/ai-tells-checklist.md)
- [Voice Techniques Reference](references/voice-techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional plaintext reports and JSON scorer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an AI-pattern audit, humanized rewrite, voice-injected draft, before/after comparison, or local humanity-score report.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
