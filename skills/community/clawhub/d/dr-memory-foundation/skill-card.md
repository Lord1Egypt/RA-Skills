## Description: <br>
Opinionated, file-based memory layout for OpenClaw-style agents: dashboards (now/open-loops/automation), topic files, glossary, and an always-on policy+topic catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to initialize or normalize file-based workspace memory for OpenClaw-style agents, including small indexes, dashboards, topic files, and daily logs. It is intended for persistent local memory setup where existing notes should be preserved and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/dr-memory-foundation) <br>
- [Apply checklist](references/APPLY.md) <br>
- [Activation prompt](references/configure_prompt.md) <br>
- [Memory template](references/templates/MEMORY.md) <br>
- [Always-on policy template](references/templates/memory/always_on.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and a Python installer for template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates missing memory template files and an initial daily log; existing files are skipped, and users should review memory content and avoid storing secrets.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
