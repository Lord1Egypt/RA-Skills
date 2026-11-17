## Description:

Execute RunningHub ComfyUI workflows via API. Use when you need to run ComfyUI workflows on RunningHub cloud platform, submit tasks, query status, and retrieve results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uiueux](https://clawhub.ai/user/uiueux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run RunningHub-hosted ComfyUI workflows, upload image inputs, monitor task status, and retrieve workflow result URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be saved to a local config file or passed on the command line.

Mitigation: Use the RUNNINGHUB_API_KEY environment variable, avoid --save-key in shared or backed-up workspaces, and rotate any key previously stored insecurely.

Risk: Image inputs are uploaded to RunningHub for workflow execution.

Mitigation: Only upload images that are acceptable to send to RunningHub and review data-handling requirements before use.

Risk: The Chrome automation script can control a browser through local Chrome remote debugging.

Mitigation: Do not run chrome_automation.py unless browser automation is intentional and the user understands it can act in a logged-in browser context.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/uiueux/skills/comfyui-runninghub)
- [RunningHub OpenAPI v2 endpoint](https://www.runninghub.ai/openapi/v2)
- [RunningHub example workflow](https://www.runninghub.ai/#/workflow/1987728214757978114)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash and Python examples; scripts return JSON task status, errors, and result URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RunningHub API key, workflow ID, and optional image path or node input parameters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
