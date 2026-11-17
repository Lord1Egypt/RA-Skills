## Description:

修复 Android 输入法中候选区、预编辑编辑器或工具面板的测量变化导致的窗口跳动、闪烁或短暂消失；适用于原生输入法宿主的布局缺陷，需要补回归测试并在模拟器验收时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[houko](https://clawhub.ai/user/houko)

### License/Terms of Use:

MIT-0

## Use Case:

Android 输入法开发者可用此技能定位原生输入法窗口边界变化引发的跳动、闪烁或短暂消失，并据此调整临时面板布局、补充打开与关闭路径的回归测试，再按项目流程完成模拟器验收。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with medium confidence, but Skillspector's review was partial because referenced files were unavailable, and its summary notes a low-probability output-handling issue.

Mitigation: Review the complete source and inspect suggested edits and commands before applying them; run device checks in the intended Android project and use synthetic test input.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/houko/skills/android-ime-window-stability)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes regression-test and Android device-verification steps; test inputs should be synthetic.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
