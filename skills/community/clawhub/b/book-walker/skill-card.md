## Description:

Interactive PDF reader for opening documents, moving through pages or blocks, searching text, managing bookmarks, and listing PDFs with natural-language commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngandsure](https://clawhub.ai/user/youngandsure)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read long PDF documents incrementally, locate sections by page or search term, and preserve reading progress with bookmarks. It is suited for text-based PDFs and optional OCR workflows when the host environment has the required tools installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening sensitive PDFs may leave extracted text, reading state, and bookmarks in local cache files.

Mitigation: Use the skill only in trusted local environments and avoid shared machines when handling sensitive documents.

Risk: Persistent free-form templates can ask the host agent to transform PDF text with LLM instructions.

Mitigation: Use only trusted templates and review template contents before applying them to document text.

Risk: Runtime dependencies and OCR tooling are installed or invoked by the host environment.

Mitigation: Review dependency installation, prefer pinned dependency versions, and install OCR tooling from trusted package sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youngandsure/skills/book-walker)
- [Publisher profile](https://clawhub.ai/user/youngandsure)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses with optional structured PDF template payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include page, block, progress, search result, bookmark, and template payload metadata.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
