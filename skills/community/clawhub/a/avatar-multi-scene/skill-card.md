## Description: <br>
Use when the user needs multiple talking-head segments, motion-transfer comparison reels, mixed host and animate clips, or multi-scene UGC with character continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pruna-ai](https://clawhub.ai/user/pruna-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative production users use this skill to plan and run Pruna-only multi-scene avatar or motion-transfer videos with cast continuity, staged reviews, and external assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pruna API credentials can be exposed if pasted into prompts, logs, or delegated work. <br>
Mitigation: Keep PRUNA_API_KEY in environment-managed secrets and avoid sharing credentials with subagents or generated command text. <br>
Risk: Paid media-generation jobs can run before the user has reviewed the plan, stills, or clips. <br>
Mitigation: Use the documented plan, stills, clips, and assembly approval gates before starting paid prediction phases. <br>
Risk: Media-processing dependencies or unpinned revisions can introduce avoidable maintenance and security risk. <br>
Mitigation: Install dependencies with current patched Pillow versions where possible and prefer pinned Git revisions for reproducible local runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pruna-ai/skills/avatar-multi-scene) <br>
- [README-INSTALL.md](README-INSTALL.md) <br>
- [Animate beats](animate-beats.md) <br>
- [Pruna API reference](references/pruna-api.md) <br>
- [Staged generation gate](references/staged-generation-gate.md) <br>
- [Workflow feedback gates](references/workflow-feedback-gates.md) <br>
- [Generation quality checklists](references/generation-quality-checklists.md) <br>
- [Skills CLI package](https://www.npmjs.com/package/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, curl examples, Python script usage, and JSON manifest patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include staged approval gates, API-key setup guidance, generated media paths, prediction IDs, and local assembly instructions.] <br>

## Skill Version(s): <br>
0.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
