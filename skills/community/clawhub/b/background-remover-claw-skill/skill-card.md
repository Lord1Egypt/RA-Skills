## Description:

Generate ai background remover images with AI via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate background-removal-style images from text prompts through the Neta AI image generation API and receive an image URL or task result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Neta API token and sends token-authenticated requests to api.talesofai.cn.

Mitigation: Use a limited or throwaway token, avoid putting secrets directly on the command line where shell history or process listings may expose them, and review the skill before installation.

Risk: The security verdict is suspicious because the skill scope is blurry and token handling is unsafe, although no malicious behavior was identified.

Mitigation: Install only from a pinned trusted revision and review the release before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barbaraledbettergq/skills/background-remover-claw-skill)
- [Neta API token page](https://www.neta.art/open/)
- [Neta API endpoint](https://api.talesofai.cn)
- [Example generated output](https://oss.talesofai.cn/picture/9499b2c5-0f8a-4c48-ae9a-1400c3b15e95.webp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime scripts print an image URL or JSON task result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and sends prompts plus token-authenticated requests to api.talesofai.cn.]

## Skill Version(s):

1.7.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
