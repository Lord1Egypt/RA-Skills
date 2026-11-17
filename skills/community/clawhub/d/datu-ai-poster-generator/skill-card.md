## Description:

This skill sends text, documents, or existing images to Datu to generate 4K information posters, perform optional deep research, and edit images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laozhangai](https://clawhub.ai/user/laozhangai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, content creators, brand operators, and knowledge-sharing teams use this skill to turn text, files, or existing poster images into high-quality information posters and follow-up image edits. Users can optionally request deep research when they need supporting background analysis and a Word report alongside the generated image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, documents, image URLs, and images to the external Datu service.

Mitigation: Use non-sensitive material first, confirm user acceptance before upload, and do not send credentials, confidential documents, or regulated data without explicit approval.

Risk: The host may store the user's Datu API key for reuse.

Mitigation: Store the key only in the host credential vault as DATU_API_KEY and avoid placing it in public code, shared documents, or ordinary chat history.

Risk: Generated results may be retained by the service for about 30 days.

Mitigation: Review the Datu privacy policy and avoid submitting content whose retention would violate user, company, or regulatory requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laozhangai/skills/datu-ai-poster-generator)
- [Datu documentation](https://datu.digilifeform.com/docs)
- [Datu homepage](https://datu.digilifeform.com)
- [Datu privacy policy](https://datu.digilifeform.com/privacy)
- [Packaged README](artifact/README.md)
- [Security and privacy notes](artifact/SECURITY.md)
- [Usage examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Files, Guidance]

**Output Format:** [Markdown responses with Datu task status, generated image URLs, and optional Word .docx research report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-controlled DATU_API_KEY sent through the X-API-Key header; generated results may be retained for about 30 days.]

## Skill Version(s):

1.1.8 (source: server release evidence, released 2026-05-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
