## Description:

Automatic graph layout using Dagre with React Flow (@xyflow/react) for auto-layout, hierarchical layouts, tree structures, and programmatic node arrangement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building React Flow interfaces use this skill to add Dagre-based automatic graph layout, configure layout direction and spacing, and avoid common coordinate-conversion and state-update mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated layout code may place nodes incorrectly if Dagre center coordinates are used directly in React Flow.

Mitigation: Convert Dagre center coordinates to React Flow top-left positions using the same node width and height values passed to Dagre.

Risk: React Flow may not update if programmatic layout reuses previous node or edge array references.

Mitigation: Commit newly created node and edge arrays after layout and run fitView after React Flow has received the updated nodes.

Risk: Large graphs can make synchronous Dagre layout slow in the browser.

Mitigation: For larger graphs, debounce layout calls, use faster Dagre rankers where acceptable, and consider running layout work in a Web Worker.

Risk: Adding @dagrejs/dagre may be unsuitable for projects with dependency, license, or bundle-size constraints.

Mitigation: Install the package only where that dependency is acceptable, and review generated layout code as normal application code before deployment.

## Reference(s):

- [Dagre Configuration Reference](reference.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/dagre-react-flow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with TypeScript, TSX, CSS, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pass/fail layout checks, configuration tables, troubleshooting guidance, and performance guidance.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
