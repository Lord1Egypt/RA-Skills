## Description: <br>
High-fidelity diagram generation (Mermaid, D2, Graphviz) for autonomous agents, with local-first rendering and persistent run history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous coding agents use this skill to turn natural-language diagram requests into Mermaid, D2, or Graphviz source and rendered diagram files. It supports iterative repair by saving each rendering attempt and compiler feedback in a run directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer invokes system package managers, npm, and a remote D2 install script. <br>
Mitigation: Review install.sh before running it, or manually install Graphviz, D2, and Mermaid CLI from trusted package managers or pinned releases. <br>
Risk: The optional cloud rendering path can send diagram content to an external service when EMERGENCE_API_KEY is configured. <br>
Mitigation: Keep confidential diagrams on the local rendering path and set EMERGENCE_API_KEY only when remote rendering is intended. <br>
Risk: Persistent run history may retain diagram source, generated images, and compiler errors under ./runs/. <br>
Mitigation: Periodically clear ./runs/ when diagrams or compiler output may contain sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergencescience/emergence-diagram-rendering) <br>
- [Publisher profile](https://clawhub.ai/user/emergencescience) <br>
- [Emergence Science](https://emergence.science) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance, diagram source code, JSON render metadata, and PNG/SVG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local rendering uses Mermaid, D2, or Graphviz when installed; render attempts are stored under ./runs/ with metadata for troubleshooting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
