## Description:

Agentizer-zh rewrites Chinese text or ongoing assistant replies into an exaggerated AI-generated style for satire and critique, using /agentizer, /agentizer-on, and /agentizer-off modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ispacekid](https://clawhub.ai/user/ispacekid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parody or critique AI-generated Chinese prose by transforming supplied text or ongoing replies into an intentionally over-structured, jargon-heavy style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Write/Edit permissions even though its primary purpose is Chinese-language style rewriting.

Mitigation: Remove or tightly scope file-writing tools unless generated output must be saved to files.

Risk: The exaggerated parody style can make serious answers less clear or inappropriately informal outside satire and critique use cases.

Mitigation: Use the skill only for intentional parody or style transformation, and keep safety and content policies higher priority than style rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ispacekid/skills/agentizer-zh)
- [AI 词汇弹药库](artifact/references/ai-vocabulary.md)
- [AI 八股套话库](artifact/references/ai-phrases.md)
- [AI 风格规则](artifact/references/ai-style-rules.md)
- [Before & After 范例集](artifact/references/examples.md)
- [humanizer](https://github.com/blader/humanizer)
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese text or Markdown-formatted rewritten prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can operate as a single-turn rewrite or as a persistent style mode until disabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
