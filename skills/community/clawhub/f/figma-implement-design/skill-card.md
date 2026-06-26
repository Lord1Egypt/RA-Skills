## Description: <br>
Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow, including design context, screenshots, assets, and project-convention translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tbeard602](https://clawhub.ai/user/tbeard602) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Figma frames, nodes, and components as production-ready code that follows the target project's design system and conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Figma MCP and OAuth access, which can expose design data to the agent workflow. <br>
Mitigation: Install only when Figma access is intended, authorize the expected Figma account, and limit use to designs the agent is allowed to inspect. <br>
Risk: The skill may download assets and propose or make code changes based on Figma content. <br>
Mitigation: Review downloaded assets and code changes before committing or deploying them. <br>


## Reference(s): <br>
- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/) <br>
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/) <br>
- [Figma Variables and Design Tokens](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma) <br>
- [ClawHub Skill Page](https://clawhub.ai/tbeard602/figma-implement-design) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with inline commands, code changes, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Figma MCP tools to retrieve design context, screenshots, and assets before producing implementation work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
