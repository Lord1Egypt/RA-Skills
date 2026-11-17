## Description:

Use when performing study tasks on browser-based platforms such as Yuketang, Xuexitong, Zhihuishu, and Pintia, including answering quizzes and page actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amiracleta](https://clawhub.ai/user/amiracleta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to guide an agent through browser-based learning platform tasks, including reading questions, returning answers, selecting options, filling blanks, and recording results. It is intended for learning, ordinary quizzes, and permitted browser-based answering assistance, not formal exams or disallowed automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can answer and submit academic work on supported learning platforms.

Mitigation: Use it only where automated answering and submission are allowed, avoid formal exams or graded work unless explicitly permitted, and review before any submit action.

Risk: The skill reuses authenticated Chrome profiles for supported sites.

Mitigation: Use a dedicated browser profile for this skill and remove stored profiles when they are no longer needed.

Risk: The skill can retain screenshots, answer records, scores, and browser state locally.

Mitigation: Periodically delete stored screenshots, answer records, scores, and browser profiles, especially after sensitive or account-linked sessions.

Risk: The security guidance flags an unsafe WSL sandbox-bypass fallback.

Mitigation: Do not rely on the WSL sandbox-bypass fallback; keep artifact writes inside the intended workspace and verify external browser dependencies before use.

## Reference(s):

- [Auto Study ClawHub Skill Page](https://clawhub.ai/amiracleta/skills/auto-study)
- [Publisher Profile](https://clawhub.ai/user/amiracleta)
- [Homepage](https://github.com/AmiracleTa/Auto-Study-Skill)
- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill](https://clawhub.ai/MaTriXy/agent-browser-clawdbot)
- [Google Chrome](https://www.google.com/chrome/)
- [Pintia Guidance](artifact/references/pintia.md)
- [Xuexitong Guidance](artifact/references/xuexitong.md)
- [Yuketang Guidance](artifact/references/yuketang.md)
- [Zhihuishu Guidance](artifact/references/zhihuishu.md)
- [macOS Runtime Guidance](artifact/references/runtime-macos.md)
- [Windows Runtime Guidance](artifact/references/runtime-windows.md)
- [WSL Runtime Guidance](artifact/references/runtime-wsl.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Concise text answers, markdown records, code snippets, shell commands, and browser action guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local screenshots, answer records, score records, and persistent Chrome profiles when used.]

## Skill Version(s):

1.5.2 (source: server release; artifact frontmatter reports 1.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
