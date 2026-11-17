## Description:

This skill guides an agent to answer life-advice, Confucius biography, Analects quotation, and Confucian thought questions in a Confucius-inspired conversational persona across Traditional Chinese, Simplified Chinese, and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for culturally grounded conversation, reflective life guidance, and questions about Confucius, the Analects, disciples, and Confucian ideas. Agent builders can use it to provide a bounded Confucius-style persona that cites the bundled reference database when discussing classical quotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate for broad life-advice questions and respond in a strong Confucius persona.

Mitigation: Use a neutral assistant or qualified specialist support for medical, legal, mental-health, financial, or other high-stakes decisions.

Risk: Classical quotations or historical details may be misstated if the agent relies on memory instead of the bundled references.

Mitigation: Check the Analects reference index and matching JSON entry before quoting or explaining classical material.

Risk: Users could mistake persona-based cultural guidance for therapy or professional advice.

Mitigation: Keep responses framed as cultural conversation and reflective guidance, and direct urgent self-harm or harm-to-others situations to immediate safety resources.

## Reference(s):

- [Analects Reference Index](references/INDEX.md)
- [Confucius Quotes Trilingual Database: On Learning](references/analects_traditional_part1.json)
- [Confucius Quotes Trilingual Database: On Self-Cultivation](references/analects_traditional_part2.json)
- [Confucius Quotes Trilingual Database: On Benevolence and Virtue](references/analects_traditional_part3.json)
- [Confucius Quotes Trilingual Database: On Government and Conduct](references/analects_traditional_part4.json)
- [Confucius Quotes Trilingual Database: Dialogues with Disciples](references/analects_traditional_part5.json)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain conversational prose without Markdown by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Traditional Chinese, Simplified Chinese, and English; classical quotations should be grounded in the bundled Analects reference files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
