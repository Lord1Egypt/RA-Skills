## Description:

Content Creation Multi Agent coordinates six content-focused agents for knowledge search, copywriting, e-commerce video scripts, image material generation, and Seedance prompt design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebao360](https://clawhub.ai/user/jiebao360)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, marketers, and OpenClaw users use this skill to configure a Feishu-connected multi-agent workflow for articles, social posts, product video scripts, image prompts and assets, and Seedance video prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and setup scripts can clone or update repositories, set executable permissions, write files under OpenClaw workspace paths, and restart the OpenClaw gateway.

Mitigation: Review scripts locally before execution, avoid curl|bash installation, and test in a non-production OpenClaw workspace first.

Risk: The bot configuration flow requests Feishu App ID and App Secret and writes them into local bot configuration files.

Mitigation: Do not paste secrets into chat, keep generated bot configs out of indexed or shared folders, and rotate any secret that may have been exposed.

Risk: Publishing scripts can change Git remotes, Git credential storage, repository contents, and public GitHub state.

Mitigation: Run publishing scripts only after reviewing their effects, use a least-privilege token, and avoid running them from unrelated repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebao360/skills/content-creation-multi-agent)
- [Publisher profile](https://clawhub.ai/user/jiebao360)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Feishu Open Platform](https://open.feishu.cn)
- [Doubao](https://www.doubao.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance, prompts, images]

**Output Format:** [Markdown, plain text, JSON configuration, shell commands, and generated prompts or assets depending on the selected agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by agent role; the package can also generate local bot configuration and setup documentation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
