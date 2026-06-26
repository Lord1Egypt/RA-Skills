## Description: <br>
Optimized desktop automation with mouse, keyboard, and screen control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niveroviero](https://clawhub.ai/user/niveroviero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to run supervised desktop workflows, including mouse and keyboard control, screenshots, image matching, window activation, clipboard operations, and optional natural-language task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control the whole desktop through mouse, keyboard, window, and application actions. <br>
Mitigation: Use it only for supervised automation, keep failsafe enabled, and enable approval mode for workflows that can change files, submit forms, or operate sensitive applications. <br>
Risk: Screenshots and clipboard reads can expose private information. <br>
Mitigation: Close sensitive windows before running the skill, limit screenshot capture to necessary regions, and treat saved screenshots or clipboard-derived data as confidential. <br>
Risk: Optional LLM planning can send screenshots to a remote or untrusted model client. <br>
Mitigation: Use trusted LLM clients only, avoid sending screenshots that contain secrets or personal data, and review generated plans before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niveroviero/desk) <br>
- [Publisher profile](https://clawhub.ai/user/niveroviero) <br>
- [Desktop Control Skill documentation](artifact/SKILL.md) <br>
- [AI Desktop Agent guide](artifact/AI_AGENT_GUIDE.md) <br>
- [Quick reference](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent use can produce desktop actions, screenshots, task plans, and saved files depending on the invoked API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
