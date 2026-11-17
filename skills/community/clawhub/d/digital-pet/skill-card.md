## Description:

数字宠物 - 一个可爱的 3D 拉布布（Labubu）数字宠物，支持互动喂食、玩耍、抚摸。用于：(1) 桌面宠物陪伴，(2) 3D 互动展示，(3) 宠物养成游戏。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wittfan](https://clawhub.ai/user/wittfan)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run a browser or desktop 3D Labubu-style virtual pet with feeding, play, petting, status, animation, and sound interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper server is exposed beyond localhost and sends wildcard CORS headers.

Mitigation: Run it only on trusted networks, bind the server to 127.0.0.1, and remove wildcard CORS before regular use.

Risk: The web views load Three.js from a live CDN without integrity checks.

Mitigation: Bundle Three.js locally or add subresource integrity and a content security policy.

Risk: The README identifies Labubu as a POP MART copyrighted character.

Mitigation: Confirm character rights and branding permissions before redistribution or commercial promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wittfan/skills/digital-pet)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with runnable HTML, JavaScript, CSS, and Python files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external API keys are required; the skill runs an interactive local web or desktop pet experience.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
