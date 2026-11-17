## Description:

ctx-shrink is a codebase analyzer that generates compact context maps for AI agents and checks for packaging and repository safety issues before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherman-os](https://clawhub.ai/user/etherman-os)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run ctx-shrink on a project, read the generated analysis, and summarize architecture, endpoints, models, dependencies, and safety findings. It is also used before publishing to identify missing gitignore protections, source maps, private files, keys, or certificates that could leak.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an externally installed, unpinned code-scanning tool over local projects.

Mitigation: Verify the upstream ctx-shrink source or use a pinned release with checksums, and confirm the executable on PATH is the intended tool before running it.

Risk: Generated context maps may expose sensitive filenames, endpoints, commit metadata, architecture details, or other project information.

Mitigation: Review AI-CONTEXT.md or any custom output before sharing it with an AI service or external recipient.

Risk: Running scans over repositories that contain live credentials can increase exposure if the resulting report is copied or transmitted.

Mitigation: Run ctx-shrink with least privilege on the intended project only, and avoid scanning repositories containing live credentials unless the work is isolated.

## Reference(s):

- [ClawHub ctx-shrink skill page](https://clawhub.ai/etherman-os/skills/ctx-shrink)
- [ctx-shrink install documentation](https://github.com/etherman-os/ctx-shrink#install)
- [ctx-shrink releases](https://github.com/etherman-os/ctx-shrink/releases)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON analysis with shell command snippets and concise remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires reading the generated ctx-shrink output file before summarizing findings; may include security and publish-safety recommendations.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
