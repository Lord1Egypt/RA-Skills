## Description:

Helps agents read anime light novels and ebooks, organize tables of contents and reading progress, summarize chapters, and recommend related titles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marson2016](https://clawhub.ai/user/marson2016)

### License/Terms of Use:

MIT-0

## Use Case:

External users and reading assistants use this skill to process uploaded anime light novels or ebooks, navigate chapters, preserve reading position during the conversation, generate chapter notes, and manage reading lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded ebooks, book titles, reading lists, and progress may reveal sensitive personal interests during an agent session.

Mitigation: Avoid uploading sensitive reading material or private reading lists unless the user is comfortable sharing them with the active agent session.

Risk: Chapter extraction and summarization can omit details or misstate plot points, especially for long chapters or image-based PDFs.

Mitigation: Review important summaries against the source text and use OCR or manual verification for image-only PDFs.

## Reference(s):

- [Anime Ebook Reader ClawHub page](https://clawhub.ai/marson2016/skills/anime-ebook-reader)
- [Anime light novel platforms and resources](references/platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reading view with tables of contents, chapter text, summaries, notes, recommendations, and progress updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first responses; may include chapter summaries, extracted key points, reading-list entries, and conversation-scoped progress state]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
