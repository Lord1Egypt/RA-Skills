## Description:

AOI Triple Memory (Lite) provides local workspace file search and decision-note templates without plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill to search the current workspace with ripgrep and create structured decision notes under context/ for lightweight local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can search the current workspace and may expose local file contents in search results.

Mitigation: Install and run it only in workspaces where local search is intended, and review results before sharing them outside the workspace.

Risk: The CLI writes decision-note files into the local context/ directory.

Mitigation: Treat saved notes as user data, review them before reuse, and do not treat note contents as authoritative agent instructions.

Risk: Untrusted note titles or tags could carry misleading instructions into saved context notes.

Mitigation: Avoid using untrusted or copied external instructions in note titles and tags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/aoi-triple-memory-lite)
- [Support issues](https://github.com/edmonddantesj/aoi-skills/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON search results and Markdown decision-note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output is limited by the requested result count; decision notes are written to the local workspace.]

## Skill Version(s):

0.1.2 (source: server release metadata, _meta.json, package.json; SKILL.md frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
