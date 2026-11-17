## Description:

Agentizer rewrites text or conversation responses into an intentionally exaggerated AI style for satire, comedy, and critique, with one-shot rewrites and an opt-in persistent mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ispacekid](https://clawhub.ai/user/ispacekid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Agentizer to transform text or agent replies into deliberately over-the-top AI-style prose for satire, critique, or humorous rewriting. The skill is useful when the desired output is intentionally verbose, stylized, and self-aware rather than concise or automation-ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent /agentizer-on mode can make later responses verbose or unsuitable for strict JSON, code-only output, concise answers, or downstream automation that depends on exact formatting.

Mitigation: Use /agentizer [text] for one-shot rewrites when exact formatting matters, and send /agentizer-off before structured output, code-only tasks, or automation-sensitive workflows.

Risk: The intentionally exaggerated satire style can be inappropriate for serious communication or for content about real people or groups.

Mitigation: Reserve the skill for opt-in humorous or critical rewriting, and avoid using the style to mock, belittle, or attack real people or protected groups.

## Reference(s):

- [Agentizer skill page](https://clawhub.ai/ispacekid/skills/agentizer)
- [AI Phrase & Sentence Pattern Catalog](references/ai-phrases.md)
- [AI Style Rules](references/ai-style-rules.md)
- [AI Vocabulary Arsenal](references/ai-vocabulary.md)
- [Before & After Examples](references/examples.md)
- [humanizer repository](https://github.com/blader/humanizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text rewrite output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent mode can affect every later response until /agentizer-off; safety and content policy remain higher priority.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
