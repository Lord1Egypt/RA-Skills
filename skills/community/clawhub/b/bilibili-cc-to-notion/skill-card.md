## Description: <br>
将B站视频字幕转换为带截图的Notion学习笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, researchers, and knowledge workers use this skill to turn Bilibili video captions into structured Notion learning notes with timestamped screenshots and embedded images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files and video-derived screenshots to Notion. <br>
Mitigation: Use a least-privilege Notion integration scoped only to the intended database and review generated content before upload. <br>
Risk: Notion pages with matching generated titles may be archived during duplicate cleanup. <br>
Mitigation: Run duplicate cleanup only when you are comfortable archiving older matching pages, and verify the target database before execution. <br>
Risk: The workflow depends on a local BBDown binary and command execution paths. <br>
Mitigation: Install BBDown from a trusted source, verify its checksum or package source, and run the skill in a controlled local environment. <br>
Risk: Passing Notion tokens directly on command lines can expose credentials through shell history or process listings. <br>
Mitigation: Prefer environment variables or a secret manager for Notion credentials and avoid pasting tokens into commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xinyuqinfeng/bilibili-cc-to-notion) <br>
- [Notion API Documentation](https://developers.notion.com/) <br>
- [BBDown Project](https://github.com/nilaoda/BBDown) <br>
- [BBDown 1.6.3 Linux x64 Release Artifact](https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_linux-x64.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown learning notes, JSON subtitle segments, screenshot image files, and Notion page creation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload local or video-derived content to Notion and return a Notion page URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
