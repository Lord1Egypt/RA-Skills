## Description:

Translates academic PDFs into readable, searchable target-language PDFs while preserving document structure, layout intent, and research meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezra-y](https://clawhub.ai/user/ezra-y)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to translate research-paper PDFs, rebuild searchable PDF outputs, localize tables and figure text, and run page-level quality review before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A cleanup path can delete files outside the job folder if a job subdirectory is replaced with a symlink.

Mitigation: Use only trusted job directories, avoid symlinks inside job render and comparison directories, and do not run candidate registration on workspaces another party can modify until the cleanup routine is fixed.

Risk: Local PDF and image processing depends on installed runtime packages.

Mitigation: Prefer pinned, hash-verified dependency installation when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ezra-y/skills/academic-pdf-translation)
- [README_EN.md](README_EN.md)
- [Quality Contract](references/quality-contract.md)
- [Routing](references/routing.md)
- [Translation Scope](references/translation-scope.md)
- [Semantic Review](references/semantic-review.md)
- [Layout Readability](references/layout-readability.md)
- [Validation](references/validation.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Searchable PDF files with Markdown status messages, JSON workspace records, and shell command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces translated PDFs in a local workspace output folder and uses hidden workspace evidence for QA and review.]

## Skill Version(s):

1.2.1 (source: release evidence, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
