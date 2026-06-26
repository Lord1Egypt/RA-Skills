## Description: <br>
aigc-images helps an agent run batch image-generation jobs through the BizyAir async API using one or more API keys, then poll and summarize generated image results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create multiple BizyAir image-generation tasks, distribute work across available API keys, poll task status, and present image URLs in Markdown. It is intended for storyboard, scene, and custom BizyAir web app image-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation parameters, and API credentials are sent to BizyAir during task creation and polling. <br>
Mitigation: Use trusted BizyAir API keys, confirm the final prompt and task count before execution, and run only when sending this data to BizyAir is acceptable. <br>
Risk: The skill supports URL-downloaded key lists and stores task state with API keys in a shared /tmp file. <br>
Mitigation: Prefer local or environment-provided keys, avoid remote key-list URLs unless fully trusted, and do not use the skill on shared machines unless temporary key storage is removed or replaced. <br>
Risk: People-related prompts may be automatically changed in a sexualized and specific way. <br>
Mitigation: Require the agent to show the final prompt before submission and remove unwanted automatic prompt additions before running generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/aigc-images) <br>
- [Publisher profile](https://clawhub.ai/user/bozoyan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown summaries with shell commands and image-result tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary task state and image URL list files under /tmp while running BizyAir jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
