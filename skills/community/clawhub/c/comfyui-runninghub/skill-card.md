## Description: <br>
Execute RunningHub ComfyUI workflows via API to submit tasks, query status, upload image inputs, and retrieve results from the RunningHub cloud platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uiueux](https://clawhub.ai/user/uiueux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to run existing ComfyUI workflows on RunningHub, including submitting jobs, uploading image inputs, polling task status, and collecting generated output URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saving an API key with --save-key stores the RunningHub credential in a local config file. <br>
Mitigation: Prefer the RUNNINGHUB_API_KEY environment variable or provide the key at runtime, and avoid committing generated config files. <br>
Risk: Image upload sends local files to RunningHub, which may expose private or regulated images to an external service. <br>
Mitigation: Upload only images approved for RunningHub processing and verify data-handling requirements before use. <br>
Risk: chrome_automation.py can control a local authenticated Chrome page through the remote debugging port. <br>
Mitigation: Run Chrome automation only when remote debugging was intentionally started for this workflow and close the debugging session afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uiueux/comfyui-runninghub) <br>
- [RunningHub website](https://www.runninghub.ai/?inviteCode=kol01-rh124) <br>
- [RunningHub OpenAPI v2 endpoint](https://www.runninghub.ai/openapi/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with bash, Python, and JSON examples; scripts print JSON API responses and output URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload local image files to RunningHub and may write task results to a JSON file when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
