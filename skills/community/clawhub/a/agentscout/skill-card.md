## Description: <br>
Discover trending AI Agent projects on GitHub and generate Xiaohongshu-ready tutorials, copywriting, hashtags, and visual assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auxito](https://clawhub.ai/user/auxito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical creators, and social content teams use AgentScout to find public AI agent projects, rank them, analyze selected repositories, and generate publish-ready Xiaohongshu posts with supporting images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected repository content, prompts, and image prompts may be sent to configured LLM or image providers. <br>
Mitigation: Use approved providers and endpoints, avoid private or sensitive repositories, and confirm provider data-handling terms before running the pipeline. <br>
Risk: GitHub access tokens may expose more repository access than the skill needs. <br>
Mitigation: Use a least-privilege GitHub token and rotate or revoke it when it is no longer needed. <br>
Risk: Generated tutorials, rankings, and social posts may contain inaccurate or misleading claims. <br>
Mitigation: Review generated analysis, copy, tags, and images before publishing or sharing externally. <br>


## Reference(s): <br>
- [AgentScout ClawHub page](https://clawhub.ai/auxito/agentscout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON metadata, shell commands, configuration guidance, and locally generated image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes analysis.md, post.md, metadata.json, and images under a local output directory for the selected project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
