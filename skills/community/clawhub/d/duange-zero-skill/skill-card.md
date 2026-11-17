## Description:

面向完全不懂 AI、不懂编程、不懂 Skill 概念的用户，使用生活化提问引导他们创建、优化、打包 Codex Skill。当用户说想做 Skill、创建小助手、把流程变成 Skill、让普通人也能写 Skill 时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifenglei](https://clawhub.ai/user/lifenglei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a Mandarin onboarding coach for turning plain-language ideas into Codex skills. It guides zero-experience users through inputs, desired outputs, safety boundaries, trigger phrases, and the files needed for a distributable skill package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills could include unsafe actions such as deletion, overwriting files, payments, authorization, publishing, or sending messages without enough user confirmation.

Mitigation: Review generated skills before distribution and require explicit confirmation for high-risk actions.

Risk: A generated or packaged skill could accidentally include credentials, private files, logs, caches, or other sensitive material.

Mitigation: Scan packages before release and exclude .env files, tokens, cookies, API keys, node_modules, caches, logs, temporary files, and personal private files.

## Reference(s):

- [Simple Conversation Flow](artifact/references/simple-conversation.md)
- [Skill Templates](artifact/references/templates.md)
- [Safety, Quality, and Packaging Checklist](artifact/references/safety-quality.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional skill files and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SKILL.md, README.md, examples.md, reference materials, scripts, assets, and manifest.json when needed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
