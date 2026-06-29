## Description: <br>
Finalize an AI-generated short film using the free Route C pipeline (Google Flow Omni Flash text-to-video, Nano Banana 2 image generation, edge-tts narration, Chrome CDP automation). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video creators use this skill to finalize AI-generated short films from storyboard assets, check shot consistency, compose 1080p videos with narration, subtitles, and music, and produce director review and fix packs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to control a browser session and reuse Chrome login state. <br>
Mitigation: Use a dedicated temporary browser profile instead of a primary logged-in profile, and review browser-control commands before execution. <br>
Risk: The bundled workflow writes local review files and scene-derived filenames from storyboard or project data. <br>
Mitigation: Run the scripts only on trusted project files, inspect storyboard input first, and keep output in a dedicated project directory. <br>
Risk: The security verdict is suspicious because the workflow is coherent but includes overbroad local automation behavior. <br>
Mitigation: Review the skill carefully before installing or running it, and limit execution to the documented video-review workflow. <br>


## Reference(s): <br>
- [Google Flow](https://labs.google/fx/tools/flow) <br>
- [Shot Consistency Checklist](references/consistency_checklist.md) <br>
- [Fallback Prompts for Problematic Shots](references/fallback_prompts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hitjcl/skills/ai-short-film-finalization) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with bash, JSON, Python, and HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When scripts are run, they can create local review assets, a self-contained HTML review console, manifest JSON, and director-fix JSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
