## Description: <br>
ClawLite Design Consult helps an agent run a product design-system consultation, propose a coherent visual direction, generate an HTML preview, and write DESIGN.md plus a CLAUDE.md design-system section. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and design-minded agents use this skill to establish or update a product design system from repository context. It is intended for guided design decisions, optional competitor research, preview generation, and documentation updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify DESIGN.md and CLAUDE.md, and CLAUDE.md can influence future agent behavior. <br>
Mitigation: Review all generated or changed files before committing, with extra attention to CLAUDE.md. <br>
Risk: Optional competitor research and preview generation may browse external sites or load Google Fonts in a local HTML preview. <br>
Mitigation: Approve browsing and preview steps only when external network access is acceptable for the project. <br>
Risk: Design recommendations may be subjective or mismatched to product constraints. <br>
Mitigation: Treat proposals as reviewable design guidance and confirm the final system before writing project documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/clawlite-design-consult) <br>
- [Publisher profile](https://clawhub.ai/user/x-rayluan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Conversational guidance with Markdown documents, shell commands, and optional HTML preview code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DESIGN.md, update CLAUDE.md, and create a local HTML preview when the user approves the design direction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
