## Description:

Chem-viz helps agents create Chinese-language interactive HTML visualizations for chemistry education, including 3D molecular structures, redox animations, equilibrium graphs, electrochemistry, process flows, crystal cells, apparatus simulations, and ionic-equilibrium views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, tutors, and chemistry-support agents use this skill to turn abstract chemistry topics into interactive local HTML pages for explanation, exploration, and validation. It is most useful when a learner needs to inspect molecular shape, electron transfer, equilibrium movement, electrochemical flow, process steps, crystal-cell counting, apparatus behavior, or ionic-balance curves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include third-party CDN scripts in some visualization paths.

Mitigation: Prefer the zero-dependency Canvas2D path and review generated HTML before sharing or opening pages that include remote CDN scripts.

Risk: Generated chemistry visualizations may be pedagogically misleading if the produced structure, curve, or numerical display is wrong.

Mitigation: Run the bundled syntax verification script and manually review the rendered page, interactions, and displayed values before using it for instruction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abill6688/skills/chem-viz)
- [Publisher profile](https://clawhub.ai/user/abill6688)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [HTML files with inline JavaScript/CSS and concise validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pages expose window.__CHEMVIZ_STATE and use the bundled verification script for syntax checks.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
