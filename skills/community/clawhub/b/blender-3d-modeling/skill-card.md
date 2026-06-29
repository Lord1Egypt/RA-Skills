## Description: <br>
Blender 3D Modeling helps agents use AgentPMT's cloud Blender service to render 3D model previews, convert model formats, check or repair printability, slice models for printing, and run reviewed Blender Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to submit 3D assets to AgentPMT-hosted Blender actions for rendering, file conversion, 3D-printability checks, mesh repair, slicing, and controlled Blender Python automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: 3D model files and related prompts are sent to AgentPMT's remote Blender service. <br>
Mitigation: Use the skill only for assets that may be shared with AgentPMT, and avoid placing secrets or sensitive data in models, prompts, scripts, or logs. <br>
Risk: The run_script action executes custom Blender Python and can upload files written to OUTPUT_DIR. <br>
Mitigation: Run only scripts that were written or reviewed for the task, keep them narrowly scoped, and save only intended outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/blender-3d-modeling) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/blender-3d-modeling) <br>
- [Action Schema](artifact/schema.md) <br>
- [AgentPMT Account Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and action parameter details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote actions may return task IDs, status JSON, signed file URLs, rendered images or videos, converted model files, G-code, and printability metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
