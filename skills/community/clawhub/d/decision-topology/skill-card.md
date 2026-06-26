## Description: <br>
Records how conversations evolve, branch, get rejected, pivot, or combine by saving structural shifts as nodes in a local JSON tree with cross-tree concept links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joncik91](https://clawhub.ai/user/Joncik91) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve the structure of exploratory conversations as local decision trees, including proposals, rejected paths, pivots, merges, and concept links that can be reviewed later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is always on by default and persistently records local conversation-structure summaries. <br>
Mitigation: Install it only when this behavior is desired; set always:false for on-demand use or delete or relocate the trees directory for tighter control. <br>
Risk: Local JSON, concept index, and markdown files may retain sensitive topic labels or structural summaries. <br>
Mitigation: Avoid using the skill for highly sensitive discussions unless local retention is acceptable, and periodically inspect or remove retained tree files. <br>


## Reference(s): <br>
- [Decision Topology on ClawHub](https://clawhub.ai/Joncik91/decision-topology) <br>
- [Decision Topology Schema v2](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the script produces local JSON tree files, markdown companions, ASCII tree views, and Mermaid diagrams.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; stores trees locally in the configured trees directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and CHANGELOG.md, released 2026-03-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
