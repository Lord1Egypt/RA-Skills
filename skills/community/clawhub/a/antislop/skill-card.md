## Description: <br>
Anti-Slop guides an agent through reviewing AI-generated content for low information density, generic phrasing, unverified claims, unnecessary structure, and lack of originality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and reviewers use this skill before publishing or sharing AI-generated content to identify low-value prose, weak analysis, false success claims, and missing evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When applied to code or PR claims, the skill may lead the agent to inspect files or run verification commands using existing workspace permissions. <br>
Mitigation: Use it in appropriately scoped workspaces and review proposed commands or file access before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/antislop) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with review checklists and verification prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install dependencies or request credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
