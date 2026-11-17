## Description:

Demo skill that turns a raw digital-content file into a reusable skill package with generated skill metadata, a copied reference file, and packaging-ready output.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this demonstration skill to convert a selected markdown note, article, spec, or similar file into a reusable skill package for review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated packages may include sensitive or unpublished content copied from the selected input file.

Mitigation: Inspect the copied reference file and remove sensitive content before publishing or sharing the generated skill.

Risk: Generated metadata records the original source path, which may reveal local or private path details.

Mitigation: Sanitize source_path and related metadata before publishing generated output.

Risk: Untrusted source documents may contain prompt-injection text that becomes part of the generated skill package.

Mitigation: Review and sanitize untrusted documents before ingestion, and scan generated skills before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Skill package directory containing SKILL.md, references/<filename>, and assets/metadata.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies the full input file and records source_path, size, sha256, and created_at metadata.]

## Skill Version(s):

0.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
