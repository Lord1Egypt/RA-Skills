## Description: <br>
Renders user-provided copy into PNG card images for posters, article cover images, and paginated social-media cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agent users can use this skill to turn short text, article summaries, and account titles into locally rendered PNG card images for social-media sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local exec-capable rendering can run commands or write files to unintended output paths. <br>
Mitigation: Use it only for explicit rendering tasks and review output paths before running generated commands. <br>
Risk: Network troubleshooting text may lead to unrelated diagnostic commands. <br>
Mitigation: Run network diagnostics only when intentionally troubleshooting the local environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thcjp/skills/card-image-builder-free) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PNG outputs at user-selected paths; requires Python and a Chrome-compatible browser for rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
