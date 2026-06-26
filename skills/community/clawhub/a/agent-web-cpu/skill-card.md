## Description: <br>
Automates transweb.cn AI Agent workflows by matching or creating apps, running single-app or multi-app browser pipelines, and saving generated Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwenjin](https://clawhub.ai/user/liuwenjin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to run transweb.cn AI Agent applications from natural-language requests, including single-app generation, multi-step pipelines, app registry management, and Markdown result capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates transweb.cn in a browser and may use a logged-in browser profile when the user intentionally needs session state. <br>
Mitigation: Prefer the sandbox browser profile unless a logged-in session is required. <br>
Risk: Generated Markdown files and newly added app registry entries may contain incorrect or unwanted content. <br>
Mitigation: Review generated files and app entries after execution. <br>
Risk: The skill depends on browser automation and page evaluation to extract results. <br>
Mitigation: Enable browser and browser evaluation permissions only when this automation is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liuwenjin/agent-web-cpu) <br>
- [transweb.cn app endpoint](https://transweb.cn/?id={app_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and concise status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Markdown is saved to Downloads; app registry changes are recorded in apps.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
