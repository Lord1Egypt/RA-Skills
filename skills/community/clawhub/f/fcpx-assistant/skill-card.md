## Description: <br>
FCPX Assistant helps automate Final Cut Pro video production workflows, including script generation, media collection, voiceover, assembly, color grading, B-roll insertion, export, publishing, and editing utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lasbder-ops](https://clawhub.ai/user/lasbder-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Video creators, editors, and automation-focused developers use this skill to plan, assemble, process, export, and publish videos with Final Cut Pro-adjacent shell scripts and a local Web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe command execution can run local shell workflows with user-supplied paths, titles, descriptions, tags, and publishing inputs. <br>
Mitigation: Audit commands before execution, avoid publishing from the Web UI until command construction is fixed, and run the skill only in a controlled local workspace. <br>
Risk: Broad automatic cleanup can remove or overwrite project outputs if run in a shared or important directory. <br>
Mitigation: Keep project outputs in a dedicated empty directory, disable or avoid auto-cleanup when reviewing behavior, and maintain backups of source media. <br>
Risk: Publishing workflows rely on sensitive platform cookies or OAuth-style credentials. <br>
Mitigation: Treat copied cookies and tokens like passwords, restrict configuration file permissions, do not commit credentials, and rotate credentials when exposure is suspected. <br>
Risk: Automated publishing can send video, title, description, tags, and account actions to the wrong destination. <br>
Mitigation: Review every upload destination, account, title, description, tag set, and draft or publish setting before allowing an upload. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lasbder-ops/fcpx-assistant) <br>
- [Dependencies guide](references/dependencies.md) <br>
- [Publishing configuration guide](references/publishing.md) <br>
- [Style and option presets](references/styles-options.md) <br>
- [Pexels API](https://www.pexels.com/api/) <br>
- [Pixabay API documentation](https://pixabay.com/api/docs/) <br>
- [DashScope OpenAI-compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks, configuration snippets, and file-oriented workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run local scripts that produce video, audio, subtitle, thumbnail, metadata, and publishing artifacts.] <br>

## Skill Version(s): <br>
3.0.0-beta (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
