## Description: <br>
macOS 上用 Hammerspoon 实现按住 Fn 切到豆包语音输入、松开切回默认输入法的自动化方案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS power users use this skill to configure a Hammerspoon workflow that switches from a default Chinese input method to Doubao voice input while Fn is held, then switches back on release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup asks users to grant Hammerspoon Accessibility and Input Monitoring permissions, which are sensitive macOS privacy permissions. <br>
Mitigation: Review the exact Hammerspoon configuration before loading it, grant permissions only if Hammerspoon and the script are trusted, and remove those permissions when the automation is no longer needed. <br>
Risk: The referenced Hammerspoon init.lua template is missing from the artifact evidence. <br>
Mitigation: Use only a reviewed Hammerspoon configuration and verify input method source IDs before reloading Hammerspoon. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heavenchenggong/fn-ime-voice-switch) <br>
- [Hammerspoon documentation](https://www.hammerspoon.org/docs/) <br>
- [Hammerspoon hs.keycodes API](https://www.hammerspoon.org/docs/hs.keycodes.html) <br>
- [Hammerspoon hs.eventtap API](https://www.hammerspoon.org/docs/hs.eventtap.html) <br>
- [Doubao input method](https://www.doubao.com/chat/ime) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and Hammerspoon Lua configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for macOS, Hammerspoon permissions, input method source IDs, and reload/testing commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
