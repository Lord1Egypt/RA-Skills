## Description: <br>
基于火山引擎豆包视频生成模型，辅助用户配置项目、确认分场景提示词，并逐步生成和合成专业短视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to plan short-form video projects, generate structured prompts for Doubao Seedance text-to-video or image-to-video workflows, confirm each scene, and assemble final videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports exposed real-looking credentials in the package. <br>
Mitigation: Do not install this version unless exposed tokens have been removed and rotated; use only limited-scope API keys. <br>
Risk: The security summary reports plaintext storage of user API keys and project data without enough safeguards. <br>
Mitigation: Avoid sensitive or private content, limit credential scope, and review local storage handling before use. <br>
Risk: The security guidance warns against the bundled GitHub publishing scripts. <br>
Mitigation: Do not run bundled publishing scripts unless they have been reviewed and are necessary for a trusted workflow. <br>
Risk: Prompts and reference materials may be sent to third-party generation services. <br>
Mitigation: Assume submitted prompts and assets leave the local environment and avoid confidential materials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cindypapa/doubao-video-creator) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Best Practices](artifact/BEST_PRACTICES.md) <br>
- [Cinematography Library](artifact/CINEMATOGRAPHY_LIBRARY.md) <br>
- [Technical Specs Guide](artifact/TECH_SPECS_GUIDE.md) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, Python snippets, JSON configuration examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of local project files, scene prompts, video task requests, and final video assembly workflows.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence, SKILL.md v3.0 notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
