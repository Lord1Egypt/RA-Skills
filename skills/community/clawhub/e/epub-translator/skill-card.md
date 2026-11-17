## Description:

Translates English EPUB files into paragraph-level Chinese bilingual editions while preserving the original text, skipping code blocks, retaining formula styling, and duplicating tables for side-by-side reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reading workflow agents use this skill to convert English EPUB books into Chinese bilingual EPUBs for side-by-side reading while preserving code, formulas, tables, and document structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a bundled API key.

Mitigation: Replace it with your own environment-provided credential before use, and rotate the bundled key if you own it.

Risk: Book contents can be sent to the configured remote translation provider.

Mitigation: Use the skill only on documents you are willing to send to that provider, and verify the configured base_url and model before running.

Risk: The script can remove an existing user-selected work directory.

Mitigation: Use a dedicated empty temporary work directory and avoid passing valuable existing folders to --work-dir.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samonysh/skills/epub-translator)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated output is a bilingual EPUB file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided EPUB and OpenAI-compatible translation configuration; supports concurrency, resume, and work-directory options.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
