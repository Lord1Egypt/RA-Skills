## Description:

Converts Chinese titles into SEO-friendly URL slugs using built-in keyword mapping or optional Pinyin transliteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and SEO practitioners use this skill to generate URL-safe slugs for Chinese blog titles, documentation pages, files, and batches of titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pinyin mode depends on the optional pypinyin package, which can introduce dependency hygiene risk if installed globally or without version control.

Mitigation: Install pypinyin in a virtual environment, prefer a pinned package version, and avoid administrator privileges during installation.

Risk: Dictionary-based conversion may produce incomplete or imprecise slugs for Chinese terms outside the built-in mapping.

Mitigation: Review generated slugs before publishing them in production URLs or documentation.

Risk: The output option writes to a user-provided path and may overwrite an existing file.

Mitigation: Choose output paths deliberately and review destination files before running with --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-slug-generator)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Plain text slugs, Markdown usage guidance, and optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-title and batch conversion; Pinyin mode requires the optional pypinyin dependency.]

## Skill Version(s):

1.2.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
