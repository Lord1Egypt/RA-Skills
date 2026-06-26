## Description: <br>
Automates Adobe After Effects using ExtendScript (.jsx) files and aerender CLI. Supports composition creation, effect application, batch rendering, project templates, and Adobe Media Encoder workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CAMEL-255](https://clawhub.ai/user/CAMEL-255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and motion-graphics engineers use this skill to automate Adobe After Effects tasks such as creating compositions, adding layers and effects, managing render queues, and producing batch renders with aerender. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the bundled or generated ExtendScript can modify the open After Effects project and render queue. <br>
Mitigation: Use copies of valuable .aep projects and review JSX scripts before running them. <br>
Risk: Batch rendering can create or overwrite render outputs in local folders. <br>
Mitigation: Choose a dedicated output folder and verify render paths before starting aerender or render-queue execution. <br>


## Reference(s): <br>
- [After Effects ExtendScript API Reference](references/extendscript_api.md) <br>
- [After Effects MCP on ClawHub](https://clawhub.ai/CAMEL-255/after-effects-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with ExtendScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSX snippets and aerender commands for local Adobe After Effects projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
