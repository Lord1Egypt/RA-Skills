## Description:

Quickly save web content as formatted Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1coos](https://clawhub.ai/user/1coos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to clip a URL from pasted text, extract readable content from supported web platforms, and save the result as local Markdown notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable third-party x-reader code from GitHub at runtime.

Mitigation: Install and use it only after reviewing and trusting the x-reader source; prefer a pinned and sandboxed extractor for stricter environments.

Risk: The skill can fetch arbitrary web addresses from the agent's network context.

Mitigation: Avoid localhost, private-network, cloud-metadata, and sensitive internal URLs unless the environment is sandboxed.

Risk: Extracted content is written to a configured local output directory.

Mitigation: Choose the output directory deliberately and review generated Markdown before sharing or importing it into other systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1coos/skills/1coos-quickie)
- [x-reader repository](https://github.com/runesleo/x-reader)
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown file plus a short text summary with output path, extracted title, and content summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports raw extractor output or Obsidian-style formatting; writes to a configured local output directory.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
