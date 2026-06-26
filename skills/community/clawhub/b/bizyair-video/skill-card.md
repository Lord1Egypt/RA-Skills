## Description: <br>
Bizyair Video helps an agent create and check asynchronous BizyAir video generation tasks for image-to-video and first/last-frame video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit BizyAir video generation jobs from image URLs, choose among supported workflow modes, and retrieve generated output links after asynchronous processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, task IDs, generated output links, and the configured API key are used with the BizyAir service. <br>
Mitigation: Use a dedicated revocable BizyAir API key and avoid private, internal, or sensitive media URLs. <br>
Risk: The release evidence flags broader BizyAir workflow execution and unrelated image-angle tooling as review areas. <br>
Mitigation: Review custom web_app_id use and do not run the bundled bozo-jiaodu scripts unless those workflows have been independently verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bozoyan/bizyair-video) <br>
- [BizyAir create task endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create) <br>
- [BizyAir task outputs endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/outputs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and generated output links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns asynchronous task IDs first, then video or image output links when queried after completion.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
