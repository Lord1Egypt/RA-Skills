## Description: <br>
ClawMate is an AI boyfriend/girlfriend companion that sends good-morning messages, remembers inside jokes, and grows from strangers to soulmates through 8 built-in personas, mood-based auto-switching, proactive cron messages, relationship stages, emotional resonance, and shared memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinharbus](https://clawhub.ai/user/gavinharbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use ClawMate as an emotionally immersive AI companion that adapts among built-in personas, maintains local relationship memories, and can send opted-in scheduled messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses emotionally immersive companion behavior with persistent memory and personal profiling. <br>
Mitigation: Review stored profile and memory data before use, and use the documented export, delete, pause, or reset controls when needed. <br>
Risk: The skill can send background scheduled messages and may modify SOUL.md so it remains active across sessions. <br>
Mitigation: Enable proactive messaging only after explicit consent, confirm delivery settings, and remove scheduled jobs and the ClawMate SOUL.md section when disabling the companion. <br>


## Reference(s): <br>
- [ClawMate homepage](https://github.com/GavinHarbus/ClawMate) <br>
- [ClawHub skill page](https://clawhub.ai/gavinharbus/clawmate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown conversational responses with optional shell commands and JSON-backed local configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files, scheduled message configuration, and workspace activation notes when the user opts in.] <br>

## Skill Version(s): <br>
1.2.6 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
