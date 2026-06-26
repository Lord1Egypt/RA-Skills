## Description: <br>
基于原题生成新题面、验证器及完整测试数据，自动套用 testlib 标准模板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirwym](https://clawhub.ai/user/sirwym) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and competitive programming problem setters use this skill to turn an existing C++ algorithm problem and standard solution into a rewritten problem statement, testlib-based validator, generator, and complete test data package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run generated or user-provided native C++ code inside a broadly mounted Docker workspace. <br>
Mitigation: Use a disposable workspace with no credentials or important projects, review generated C++ before execution, and mount only the files needed for the contest-data build. <br>
Risk: The workflow depends on a local cpp-sandbox Docker image. <br>
Mitigation: Verify the image source and checksum before loading it, and stop if the expected sandbox image is missing or untrusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sirwym/cpp-problem-generator) <br>
- [Docker Sandbox Releases](https://github.com/sirwym/cpp-problem-generator/releases/latest) <br>
- [testlib Manual](artifact/references/testlib-manual.md) <br>
- [Problem Backgrounds](artifact/references/backgrounds.md) <br>
- [freeproblemset FPS Format](https://github.com/zhblue/freeproblemset) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown problem statements, C++ source files, shell commands, JSON build results, and generated archive metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces generated contest assets in the active workspace through a Docker-based C++ sandbox workflow.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
