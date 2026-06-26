## Description: <br>
Agentlens helps agents navigate and understand codebases using project-local AgentLens hierarchical documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nguyenphutrong](https://clawhub.ai/user/nguyenphutrong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use Agentlens to navigate large codebases through generated .agentlens maps, locate modules and symbols, review TODOs and warnings, and choose source sections to inspect before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .agentlens documentation may be stale or incomplete. <br>
Mitigation: Verify important guidance from .agentlens files against the actual source code before making changes. <br>
Risk: Regenerating documentation requires running an agentlens command in the local environment. <br>
Mitigation: Confirm the command resolves to the trusted AgentLens CLI before allowing the agent to execute it. <br>


## Reference(s): <br>
- [Navigation Patterns](references/navigation.md) <br>
- [AgentLens Output Structure](references/structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown instructions with file paths and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Relies on project-local .agentlens documentation when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
