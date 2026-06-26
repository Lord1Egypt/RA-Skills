## Description: <br>
A VR panorama operations assistant for configuring 9kvr account credentials and managing panorama works, media, scenes, hotspots, background music, voice narration, ratings, and integration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianming3](https://clawhub.ai/user/tianming3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External panorama content operators, project delivery teams, and developers use this skill to manage 9kvr panorama projects through guided CLI actions and workflow instructions. It supports account setup, content and scene configuration, audio narration, ratings checks, and integration-code guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles uid/token account credentials. <br>
Mitigation: Use scoped or test tokens where possible, avoid exposing secrets in shared chats or terminals, and rotate tokens if they are exposed. <br>
Risk: The skill may install and run an external VRAPI helper binary. <br>
Mitigation: Install only when the publisher, the 9kvr service, and the helper binary delivery path are trusted. <br>
Risk: Generated integration code may expose developer keys or sensitive playback links if copied directly to client-side code. <br>
Mitigation: Review generated integration code and keep developer keys server-side, using a server proxy where appropriate. <br>
Risk: Delete or bulk-update actions can affect panorama media, scenes, or hotspots. <br>
Mitigation: Require explicit confirmation before destructive or bulk changes and verify results with a follow-up read. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianming3/9kvr-panorama) <br>
- [9kvr official site](https://9kvr.cn) <br>
- [Router reference](references/router.md) <br>
- [Commands reference](references/commands.md) <br>
- [Workflow reference](references/workflows.md) <br>
- [Examples reference](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose API-backed actions for 9kvr resources and should verify write operations with follow-up reads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
