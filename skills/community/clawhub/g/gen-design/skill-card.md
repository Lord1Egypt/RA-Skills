## Description: <br>
Generates system design documents through interactive technology selection, domain-knowledge-driven data model and integration design, and alignment with PRD data flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lf951515851](https://clawhub.ai/user/lf951515851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system architects use this skill to turn PRDs or clear requirements into implementation-ready system design documentation, including architecture, technology stack, modules, APIs, data models, deployment, and required data-flow integration sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a design document under docs/design and may offer to continue into validation. <br>
Mitigation: Use it in repositories where documentation file creation is expected, and explicitly pause or opt out if only the design document should be generated. <br>
Risk: Generated architecture, API, and data-model recommendations may be inaccurate or incomplete for a specific project context. <br>
Mitigation: Review the generated design against the PRD, repository constraints, and domain requirements before using it for implementation planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lf951515851/gen-design) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Prompt](artifact/prompt.md) <br>
- [Design template](artifact/design-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown design document written to docs/design/YYYY-MM-DD-{project-name}-design.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mermaid diagrams, API tables, ER models, integration contracts, and follow-up validation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
