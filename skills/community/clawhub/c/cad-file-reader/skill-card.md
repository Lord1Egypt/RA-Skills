## Description:

读取 DWG/DXF，提取标注、几何证据、图层/块语义、MEP 拓扑、图纸对比、钢结构/市政识图候选和规范图集索引；不输出最终工程量。

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Developers and engineering teams use the skill to inspect construction drawings and extract traceable text, geometry, topology, and measurement candidates for review. Its results are evidence and candidates, not final quantities or engineering sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with high confidence; its partial scan reports broad, undeclared capabilities and setup actions beyond the stated drawing-reading purpose.

Mitigation: Review setup steps and file-access scope before installation, and install only if the capabilities are needed. The scan covered 186 of 191 components, so unreported behavior remains unassessed.

Risk: Release metadata and the bundled artifact disagree on license and version: the server evidence lists MIT-0 and 0.41.4, while LICENSE.md and SKILL.md state CC-BY-NC-SA-4.0 and 0.42.0.

Mitigation: Confirm the applicable license and that the bundled files match the intended release before use.

## Reference(s):

- [CAD 图纸识图 on ClawHub](https://clawhub.ai/lisong2003-lgtm/skills/cad-file-reader)
- [License terms (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- [Reliability guidance](artifact/docs/reliability.md)
- [Detailed usage reference](artifact/references/on-demand.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured JSON evidence and candidate records, with text or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source coordinates, confidence and review flags where available; measurement values remain candidates and final_quantity is false.]

## Skill Version(s):

0.41.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
