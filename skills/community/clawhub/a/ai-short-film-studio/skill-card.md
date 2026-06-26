## Description: <br>
Ai Short Film Studio guides agents through low-cost AI short-film production workflows covering storyboarding, prompt design, batch video generation, TTS, subtitles, audio mixing, review, and delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and developers use this skill to plan, generate, assemble, and iterate AI short films, short drama episodes, trailers, and educational videos. It is intended for agents that can propose production plans, generate scripts and prompts, run helper commands, and coordinate media assembly workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can automate logged-in Chrome sessions through remote debugging. <br>
Mitigation: Use a dedicated Chrome profile, close remote debugging after use, and review automation steps before running them. <br>
Risk: Batch video and TTS generation can consume paid credits and write many local media files. <br>
Mitigation: Confirm API calls, quotas, prompts, and output directories before execution, and monitor generated files during long runs. <br>
Risk: The artifact includes cloud storage guidance that should not be reused as-is. <br>
Mitigation: Replace any listed storage identifiers with an owned, least-privilege storage setup and keep secrets outside shared skill files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hitjcl/ai-short-film-studio) <br>
- [Production Workflow Reference](references/production_workflow.md) <br>
- [Sucuang API Reference](references/sucuang_api.md) <br>
- [Google Flow](https://labs.google/fx/tools/flow) <br>
- [Sucuang API Documentation](https://api.wuyinkeji.com/doc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and helper script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce project files, storyboard JSON, generated media commands, and post-production instructions for user review.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
