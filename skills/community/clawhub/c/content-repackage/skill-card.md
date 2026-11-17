## Description:

Convert markdown content into Twitter threads, email digests, and standalone HTML landing pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiuannnn](https://clawhub.ai/user/zhiuannnn)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, newsletter authors, developers, and marketers use this skill to repackage one markdown source into channel-specific publishing assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package appears incomplete because required local helper modules are missing, so the script may fail before generating output.

Mitigation: Confirm the publisher supplies the required markdown parser and generator modules before relying on the release.

Risk: The script reads a user-selected markdown file and writes generated files to an output directory.

Mitigation: Run it only against intended input files and review the generated files before publishing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhiuannnn/skills/content-repackage)

## Skill Output:

**Output Type(s):** [text, code]

**Output Format:** [Plain text and standalone HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a Twitter thread text file, an email digest text file, and an HTML landing page to the selected output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
