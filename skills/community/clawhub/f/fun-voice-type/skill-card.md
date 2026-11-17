## Description:

A macOS voice input skill that uses Alibaba Cloud FunASR real-time speech recognition to turn speech captured while holding Right Option into typed text, with optional translation into multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzwu2017](https://clawhub.ai/user/yzwu2017)

### License/Terms of Use:

MIT-0

## Use Case:

External users on macOS use this skill to dictate text into the currently focused application and optionally translate spoken input before insertion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microphone audio and translated text may be sent to DashScope/Qwen cloud services.

Mitigation: Avoid dictating secrets or regulated information, and use the skill only where cloud processing of speech content is acceptable.

Risk: The running process can type into any focused application after Accessibility and Input Monitoring permissions are granted.

Mitigation: Grant macOS privacy permissions only to a trusted terminal or Python process and stop the tray app when voice typing is not needed.

Risk: Runtime dependencies and macOS privacy permissions expand the local execution surface.

Mitigation: Install dependencies in a virtual environment with pinned versions before granting Microphone, Accessibility, and Input Monitoring permissions.

## Reference(s):

- [DashScope Console](https://dashscope.console.aliyun.com/)
- [ClawHub skill page](https://clawhub.ai/yzwu2017/skills/fun-voice-type)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands; runtime output is typed text in the focused macOS application.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DashScope API key plus macOS Microphone, Accessibility, and Input Monitoring permissions.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
