## Description: <br>
Intelligent skill orchestrator that compiles natural language requests into secure, reusable workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bvinci1-design](https://clawhub.ai/user/bvinci1-design) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use Flow to turn natural language workflow ideas into reusable composed skills, with registry lookup, component scanning, and generated Python workflow files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated executable Python workflows can be created and registered from broad natural language input without sufficient validation or rescanning. <br>
Mitigation: Install and run Flow in an isolated environment, review generated files under the configured flows directory and skill_registry.json before reuse, and rescan generated workflows before deployment. <br>
Risk: A displayed PASSED status may reflect only a component scan and not proof that the final generated workflow is safe. <br>
Mitigation: Treat scan status as one input to review, disable automatic registry updates when appropriate, and pin dependencies before production use. <br>


## Reference(s): <br>
- [Flow on ClawHub](https://clawhub.ai/bvinci1-design/flow) <br>
- [Publisher profile](https://clawhub.ai/user/bvinci1-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output, Markdown skill definitions, JSON-style result objects, and generated Python workflow files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated flows may be written to the configured flows directory and optionally registered in skill_registry.json.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
