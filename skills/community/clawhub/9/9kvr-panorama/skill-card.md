## Description:

芊云VR全景运营小助手 helps agents manage 9KVR panorama projects, including account setup, works, media, scenes, hotspots, background music, voiceovers, ratings, and integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianming3](https://clawhub.ai/user/tianming3)

### License/Terms of Use:

MIT-0

## Use Case:

Panorama content operators, project delivery staff, and developers use this skill to manage VR panorama content, configure scenes and media, add audio assets, review ratings, and generate integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unverified native 9KVR client with user credentials.

Mitigation: Install only when the publisher and native client are trusted, and avoid sharing long-lived uid/token values unless necessary.

Risk: Generated integration guidance may place developer secrets in browser-visible code.

Mitigation: Review generated code before use and keep developer secrets on the server side.

Risk: Uploads, deletes, or account-changing actions can modify a user's VR panorama content or session state.

Mitigation: Require explicit confirmation before these actions and verify results afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianming3/skills/9kvr-panorama)
- [9KVR official site](https://9kvr.cn)
- [9KVR developer documentation](https://9kvr.cn/user/develop/welcome)
- [README](README.md)
- [Routing reference](references/router.md)
- [Command reference](references/commands.md)
- [Workflow reference](references/workflows.md)
- [Examples reference](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, code snippets, and structured command results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform account configuration, uploads, deletes, and service changes through the 9KVR native client when the user provides credentials and confirms the action.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
