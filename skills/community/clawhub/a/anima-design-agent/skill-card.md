## Description: <br>
Anima helps agents turn prompts, website URLs, Figma designs, or Anima playgrounds into live hosted apps or generated code for existing projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-focused agents use this skill to create hosted web app prototypes, clone website experiences, convert Figma designs, publish Anima playgrounds, or generate design-aware code for an existing codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad build requests can lead to live published apps or local code changes without clear confirmation. <br>
Mitigation: Make publish or deploy intent explicit, and review generated files and write locations before execution. <br>
Risk: Prompts, Figma designs, and private URLs may be sent to Anima as an external design, code-generation, and hosting service. <br>
Mitigation: Use only data approved for Anima, and avoid confidential designs or private URLs unless that service is approved for the data. <br>
Risk: The skill requires ANIMA_API_KEY for headless use. <br>
Mitigation: Provide ANIMA_API_KEY only through a secure environment variable or secret store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dannyshmueli/anima-design-agent) <br>
- [Anima MCP server guide](https://github.com/AnimaApp/mcp-server-guide) <br>
- [Anima CLI documentation](https://github.com/AnimaApp/anima-cli) <br>
- [Anima MCP documentation](https://docs.animaapp.com/docs/integrations/anima-mcp) <br>
- [Anima MCP setup guide](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline CLI and MCP examples, plus generated application code or hosted playground links when tools are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require ANIMA_API_KEY and Anima account access; Figma flows may require connected Figma authorization.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
