## Description: <br>
Runs Coze workflows through the Coze API for automation tasks such as image generation, data processing, and text analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjin714](https://clawhub.ai/user/hanjin714) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to authenticate with Coze, list known workflows, invoke selected workflow IDs, and process returned text, Markdown, image URLs, or downloaded files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs may be sent to remote Coze workflows under a local service token. <br>
Mitigation: Use only trusted Coze workspaces and avoid personal, proprietary, or regulated data unless external processing is acceptable. <br>
Risk: The runner reads credentials from a hardcoded local token path. <br>
Mitigation: Replace the hardcoded path with an explicit least-privilege secret before use. <br>
Risk: Workflow IDs may trigger side effects or return files from remote services. <br>
Mitigation: Verify each workflow ID, expected side effects, and output destination before invoking or downloading results. <br>


## Reference(s): <br>
- [Coze workflow list reference](references/workflows.md) <br>
- [Coze workflow project](https://www.coze.cn/space/7555350866765545515/project-ide/7610360135081295918) <br>
- [Coze workflow API endpoint](https://api.coze.cn/v1/workflow/run) <br>
- [ClawHub skill page](https://clawhub.ai/hanjin714/coze-workflow-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown, Python examples, shell commands, workflow response text, and downloadable file URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send supplied input to remote Coze workflows and may download returned image files when instructed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
