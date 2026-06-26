## Description: <br>
Fableforge is a command-level SOP that guides an agent through concept development, scripting, voice generation, asset preparation, timeline construction, HyperFrames rendering, and publishing for short-form video production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developer-agents use this skill to produce structured short-form videos from idea selection through rendered output and release packaging. It is most relevant when the agent is expected to coordinate scripts, audio, generated images or B-roll, HTML/CSS composition, and command-line rendering steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can install tools, download dependencies, and run command-line video tooling. <br>
Mitigation: Review dependency sources and command effects before execution, and run setup in an isolated project environment. <br>
Risk: The workflow may use a personal voice clone and voice samples. <br>
Mitigation: Require explicit speaker consent before voice cloning and keep voice sample files out of version control. <br>
Risk: The workflow changes local project files and may create Git history. <br>
Mitigation: Inspect git status and diffs before any commit or push, and require user approval before publishing changes. <br>


## Reference(s): <br>
- [Fableforge ClawHub release](https://clawhub.ai/lucas-kay8/fableforge) <br>
- [Publisher profile](https://clawhub.ai/user/lucas-kay8) <br>
- [Skill definition](artifact/SKILL.en.md) <br>
- [Stage workflow documentation](artifact/resources/stages/) <br>
- [Voice model recording guide](artifact/resources/voice-model/README.md) <br>
- [Visual style bible](artifact/resources/style_bible.md) <br>
- [Troubleshooting manual](artifact/resources/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline code, shell commands, HTML/CSS templates, and production checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged workflow artifacts such as scripts, narration metadata, asset plans, timeline configuration, render commands, and publishing notes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
