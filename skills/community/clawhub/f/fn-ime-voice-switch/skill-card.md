## Description:

Guides macOS users through configuring Hammerspoon so holding Fn switches to Doubao voice input and releasing Fn returns to the default input method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

External macOS users use this skill to set up a one-key workflow for switching between their regular Chinese input method and Doubao voice input. It provides installation, permission, input-source lookup, Hammerspoon configuration, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to grant Hammerspoon Accessibility and Input Monitoring permissions and run a persistent local configuration.

Mitigation: Install only when those permissions are acceptable, review the Hammerspoon configuration before enabling it, and keep existing ~/.hammerspoon/init.lua content unless the change is understood.

Risk: The reviewed artifact references templates/init.lua, but that Lua template is missing from the artifact.

Mitigation: Obtain and inspect the missing template from a trusted source before applying the configuration.

## Reference(s):

- [Hammerspoon Documentation](https://www.hammerspoon.org/docs/)
- [Hammerspoon hs.keycodes API](https://www.hammerspoon.org/docs/hs.keycodes.html)
- [Hammerspoon hs.eventtap API](https://www.hammerspoon.org/docs/hs.eventtap.html)
- [Doubao Input Method](https://www.doubao.com/chat/ime)
- [ClawHub Skill Page](https://clawhub.ai/heavenchenggong/skills/fn-ime-voice-switch)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and Lua configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is tailored around a required default input method source ID and local macOS permission state.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
