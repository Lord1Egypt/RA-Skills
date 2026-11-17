## Description:

Chinese Ebook Downloader helps agents find and download Chinese-language ebooks from multiple sources with automatic fallback, optional EPUB-to-PDF conversion, and support for PDF, EPUB, MOBI, and AZW3 formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lb1121](https://clawhub.ai/user/lb1121)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to locate and download Chinese-language ebooks, including batch workflows and format conversion when EPUB content needs PDF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts third-party ebook and file-hosting sites, which can reveal requested titles and file-host passwords.

Mitigation: Use only content the user is authorized to access, avoid broad auto-trigger use, and use a unique throwaway file-host password.

Risk: The skill downloads and extracts untrusted files and may overwrite or delete local outputs.

Mitigation: Run the skill in a sandbox with limited filesystem and network access and review output paths before batch runs.

Risk: The skill converts untrusted EPUB content with weak sandboxing.

Mitigation: Convert files only in an isolated environment and treat converted documents as untrusted until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lb1121/skills/chinese-ebook-downloader)
- [Playwright documentation](https://playwright.dev/)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated local ebook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, overwrite, delete, extract, or convert local ebook files during scripted workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
