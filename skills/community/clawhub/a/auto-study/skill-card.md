## Description: <br>
Use when performing study tasks on browser-based platforms such as Yuketang, Xuexitong, Zhihuishu, and Pintia, including answering quizzes and page actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amiracleta](https://clawhub.ai/user/amiracleta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide a browser-based agent through study-platform workflows, including reading questions, returning answers, selecting or filling responses, and optionally submitting when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent control of a logged-in browser profile and can submit quiz or coursework answers. <br>
Mitigation: Use only for permitted practice or coursework assistance, require explicit user confirmation before submission, and review every answer before applying it. <br>
Risk: The skill may save screenshots, markdown records, scores, and browser profile data from study platforms. <br>
Mitigation: Use a dedicated browser profile and delete saved screenshots, records, scores, and profiles after the task is complete. <br>
Risk: Automation may violate rules for formal exams, contests, or platforms that prohibit automated assistance. <br>
Mitigation: Do not use the skill for formal exams, contests, or prohibited platform workflows. <br>


## Reference(s): <br>
- [Auto Study ClawHub listing](https://clawhub.ai/amiracleta/auto-study) <br>
- [Project homepage from metadata](https://github.com/AmiracleTa/Auto-Study-Skill) <br>
- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser Skill](https://clawhub.ai/MaTriXy/agent-browser-clawdbot) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>
- [Core strategy](artifact/SKILL.md) <br>
- [Xuexitong-specific strategy](artifact/references/xuexitong.md) <br>
- [Zhihuishu-specific strategy](artifact/references/zhihuishu.md) <br>
- [Yuketang-specific strategy](artifact/references/yuketang.md) <br>
- [Pintia-specific strategy](artifact/references/pintia.md) <br>
- [Windows runtime instructions](artifact/references/runtime-windows.md) <br>
- [WSL runtime instructions](artifact/references/runtime-wsl.md) <br>
- [macOS runtime instructions](artifact/references/runtime-macos.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, concise answer text, browser action guidance, and optional code or shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save markdown records, screenshots, answer records, and scores under the configured auto-study workspace.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
