## Description:

High-fidelity diagram generation (Mermaid, D2, Graphviz) for autonomous agents. Supports local-first rendering and persistent run history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn natural language or diagram source code into Mermaid, D2, and Graphviz visuals for architectures, flows, schemas, and graph-style diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make privileged system-wide package changes and run an unverified remote D2 installer.

Mitigation: Review install.sh before use, avoid running it on sensitive machines, and prefer manually installing pinned Graphviz, D2, and Mermaid CLI binaries.

Risk: Cloud fallback can send diagram content and an API key to a render endpoint when local renderers are unavailable.

Mitigation: Use a local-only workflow for sensitive diagrams and configure cloud rendering only when data sharing is intended.

Risk: Persistent render history can retain diagram source, compiler output, and generated images.

Mitigation: Review and clean the runs directory before sharing the workspace or artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergencescience/skills/emergence-diagram-rendering)
- [Emergence Science](https://emergence.science)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with diagram source code, renderer commands, and generated image or metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local render attempts are written under a runs directory with input, output, and metadata files.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact/SKILL.md frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
