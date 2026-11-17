## Description:

Track game design prototype ideas, branching outcomes, dead ends, baselines, and next experiments, and optionally generate a simple SVG visualization of prototype evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Game designers, developers, and product teams use this skill to preserve prototype learning as branching design memory, including chosen paths, parked ideas, dead ends, backtrack notes, and next experiments. When a visual map is useful, the agent can create branch-map JSON and run the bundled SVG renderer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prototype logs or branch maps could be written outside the intended project area if the output path is not reviewed.

Mitigation: Keep generated files in a controlled project or output directory and review paths before running the SVG renderer.

Risk: Prototype records may preserve assumptions or dead-end labels that later become outdated.

Mitigation: Review generated logs and maps before relying on them for roadmap, production, or team decisions.

## Reference(s):

- [Branch Map Format](references/branch-map-format.md)
- [Example Branch Map](references/example-branch-map.json)
- [State Labels](references/state-labels.md)
- [ClawHub skill page](https://clawhub.ai/stanestane/skills/game-design-prototyping-companion)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, code, guidance]

**Output Format:** [Markdown guidance with optional JSON branch-map files, shell commands, and SVG file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local files for prototype logs, branch-map JSON, and SVG visualizations when requested.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
