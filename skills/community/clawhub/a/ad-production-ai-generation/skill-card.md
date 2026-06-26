## Description: <br>
AI生成 helps agents manage AI generation tasks for advertising creative, including copy, marketing images, video assets, and batch creative materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and advertising teams use this skill through an agent to create, inspect, cancel, and select AI-generated ad creative materials from prompts and generation parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters may expose confidential campaign details or other sensitive task data. <br>
Mitigation: Treat prompts and generation parameters as visible task data and avoid entering secrets or confidential campaign information. <br>
Risk: Batch creative generation can create excessive volume in shared or high-throughput environments. <br>
Mitigation: Apply count limits, concurrency limits, and per-user scoping when operating the skill in shared or high-volume settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JEyeshield/ad-production-ai-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [OpenClaw action responses and events containing task IDs, task status, generated material metadata, prompts, model names, parameters, and optional quality scores.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation results may include multiple candidates per task and support selecting, rejecting, listing, cancelling, and ranking results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
