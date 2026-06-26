## Description: <br>
An iterative, high-rigor presentation generation skill leveraging Marp and the Emergence Render API for Agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and presentation authors use this skill to iteratively plan slide decks, draft Marp Markdown, render diagrams through the Emergence API, and compile presentations to PDF, PPTX, or HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive diagram, CSV-derived, or presentation content may be sent to the third-party Emergence rendering service. <br>
Mitigation: Review the skill before installing, avoid sending confidential presentation material unless approved, and use the rendering API only with data suitable for that service. <br>
Risk: The skill requires an Emergence API key and uses it for rendering requests. <br>
Mitigation: Provide EMERGENCE_API_KEY only when the service is trusted for the intended use case and manage the key as a sensitive credential. <br>
Risk: Marp compilation may execute through an unpinned npx command in the artifact examples. <br>
Mitigation: Prefer a pinned or locally controlled Marp renderer for sensitive or production presentation workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/emergencescience/emergence-ppt-orchestra) <br>
- [Publisher Profile](https://clawhub.ai/user/emergencescience) <br>
- [Marp](https://marp.app/) <br>
- [Emergence Render API OpenAPI](https://api.emergence.science/tools/render/openapi.json) <br>
- [Emergence Content Index](https://emergence.science/content/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown deck files with rendered image assets and shell commands for Marp compilation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce presentation.md, assets, PDF, PPTX, or HTML outputs depending on the user's requested deck format.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
