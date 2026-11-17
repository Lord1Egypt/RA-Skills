## Description:

Builds deterministic Excalidraw drawings from a boxes-and-arrows spec, with layout and bindings. Produces Obsidian .excalidraw.md notes or .excalidraw files. Use only for explicit Excalidraw requests, including Excalidraw in Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can turn a boxes-and-arrows specification into an editable Excalidraw diagram for excalidraw.com or an Obsidian note. The skill lays out and binds diagram elements, then provides structural validation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a diagram specification and writes a drawing to a selected path; using --force can replace an existing file.

Mitigation: Use a trusted specification, check the destination path, and use --force only when you intend to replace that file.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ricardodpalmeida/skills/excalidraw-diagrams)
- [Project homepage](https://github.com/Ricardodpalmeida/openclaw-excalidraw-diagrams)
- [Excalidraw file format reference](artifact/references/excalidraw-format.md)
- [Excalidraw editor](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown]

**Output Format:** [Editable Excalidraw scene JSON (.excalidraw) or an Obsidian Markdown note (.excalidraw.md)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic layout, labels, and bindings generated from a boxes-and-arrows specification.]

## Skill Version(s):

1.1.10 (source: release metadata, CHANGELOG.md, released 2026-11-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
