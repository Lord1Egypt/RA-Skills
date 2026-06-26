## Description: <br>
Enables an agent to inspect a desktop screen and operate mouse, keyboard, OCR, image matching, and screenshot workflows through OpenClaw Node and pyautogui. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncsimok](https://clawhub.ai/user/ncsimok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate desktop applications, file workflows, and visual UI interactions that require screen inspection, OCR, mouse movement, clicking, dragging, keyboard input, and result verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can view the desktop and operate the mouse and keyboard, which can expose sensitive windows or account workflows. <br>
Mitigation: Use only when desktop control is intended, keep sensitive windows closed, and supervise actions involving accounts, payments, posting, deletion, or configuration changes. <br>
Risk: Screen automation can click or type in the wrong place when the visual state changes or OCR/image matching is inaccurate. <br>
Mitigation: Capture and review screenshots before action, confirm destructive operations with the user, and verify results with a follow-up screenshot. <br>
Risk: Persistent administrator service mode can leave ongoing node access available beyond a bounded session. <br>
Mitigation: Prefer explicit command-line pairing for normal use and avoid persistent administrator service mode unless ongoing node access is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ncsimok/doorstep-screen-control) <br>
- [Screen Control setup guide](references/setup-guide.md) <br>
- [Tesseract OCR setup reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON command responses, and screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshot files and JSON status outputs while controlling the local desktop.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
