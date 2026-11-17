## Description:

Turn a shower idea into a full best-seller manuscript in one command, using a multi-stage writing pipeline that produces a manuscript and Amazon KDP publishing package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipstark](https://clawhub.ai/user/philipstark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to turn a book concept into a generated manuscript, editorial memo, and Amazon KDP launch package for fiction or non-fiction projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send book ideas and generated manuscript material to Anthropic.

Mitigation: Use it only with content that is acceptable to process under the user's Anthropic account terms, and avoid sensitive unpublished or personal material unless that sharing is acceptable.

Risk: Long generation runs can spend API credits.

Mitigation: Review model, chapter, and batch settings before running, and start with a smaller chapter count when cost exposure needs to be limited.

Risk: The CLI creates many local files.

Mitigation: Set an explicit output directory and review generated files before publishing or sharing them.

Risk: Dependency installation is not pinned by a lockfile in the submitted artifact.

Mitigation: Pin dependencies with a lockfile before running npm install in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/philipstark/skills/bestseller-writer)
- [Publisher Profile](https://clawhub.ai/user/philipstark)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, command-line output, and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a manuscript, KDP package, plan, character or authority notes, and editorial memo in a local output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
