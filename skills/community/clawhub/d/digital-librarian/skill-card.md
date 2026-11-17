## Description:

Librarian ingests user-provided URLs or files, identifies media type and intent, summarizes key details, tags the content, and saves a structured Markdown note in a personal Obsidian-style library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earu723](https://clawhub.ai/user/earu723)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save articles, videos, PDFs, images, podcasts, and other shared content into a structured personal knowledge library for later reference, analysis, or downstream creative work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive URLs and files may be fetched, summarized, and stored in local library notes.

Mitigation: Use the skill only with content appropriate for local storage, and review saved notes before sharing or syncing the library folder.

Risk: X/Twitter links are fetched through FxTwitter, which may expose the shared URL to that service.

Mitigation: Avoid using private or sensitive X/Twitter URLs with this workflow, and review fetched content before relying on the note.

Risk: Some media types may produce incomplete notes when transcripts, full text, or audio transcription are unavailable.

Mitigation: Treat those notes as summaries of available metadata unless the user supplies the missing transcript or source text.

## Reference(s):

- [Media Type Fetch Strategies](references/media-types.md)
- [ClawHub Skill Page](https://clawhub.ai/earu723/skills/digital-librarian)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown note file plus concise text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes notes under library/YYYY-MM-DD-[slug].md and may include a follow-up prompt when user intent is unclear.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
