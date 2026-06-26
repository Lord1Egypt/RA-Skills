## Description: <br>
Sora2 Video helps agents submit text-to-video generation jobs through the Tianshu proxy and fetch generated results by task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working with TsClaw or OpenClaw use this skill to create Sora2 text-to-video jobs, then poll task status and generated result metadata through configured proxy URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters are sent to the configured video API or proxy and may contain sensitive private content. <br>
Mitigation: Review prompts before execution and avoid sending confidential, regulated, or private content unless the destination is approved. <br>
Risk: The skill uses bearer credentials and may trigger paid or quota-consuming video generation requests. <br>
Mitigation: Use least-privilege credentials, keep TS_TOKEN out of logs and source files, and review requests before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/aiznt-sora2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS; submit returns a task payload, and fetch returns task status or generated result metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
