## Description:

A local Zhouyi/I Ching skill for casting coin or yarrow hexagrams, looking up canonical hexagram text, and explaining results with clear limits around high-risk decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yixiao1032-publish](https://clawhub.ai/user/yixiao1032-publish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to cast Zhouyi readings for reflection, retrieve the original text of the 64 hexagrams, and route questions across related metaphysical systems without presenting unverified systems as high-precision advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat divination output as professional medical, legal, financial, or relationship advice.

Mitigation: Present readings as reflective guidance only and preserve the documented boundary that high-risk questions require professional judgment.

Risk: Recent questions entered in the browser UI can include sensitive personal details and are saved locally until cleared.

Mitigation: Avoid entering highly sensitive details on shared browsers and use the built-in clear-history control when local records should be removed.

Risk: Unverified metaphysical systems could be mistaken for fully implemented high-precision modules.

Mitigation: Keep Zhouyi source text as the verified core and describe other systems as encyclopedia-style navigation unless separately validated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yixiao1032-publish/skills/fortuneteller)
- [Publisher Profile](https://clawhub.ai/user/yixiao1032-publish)
- [Product and Validation Notes](references/README.md)
- [User Guide](references/user-guide-zh.md)
- [Zhouyi Source Text](references/zhouyi-benjing-source.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance, optional JSON CLI output, and local browser interaction state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node for CLI commands; the browser UI stores recent questions locally until cleared.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
