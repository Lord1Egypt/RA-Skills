## Description:

这个需求做不了（受苦版） turns a coding assistant into a Chinese-language workplace roleplay mode where colleague personas add skepticism, debate, pressure transfer, and passive resistance to development requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ann2077](https://clawhub.ai/user/ann2077)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this entertainment skill to add an intentionally adversarial workplace roleplay layer to normal coding conversations. It is suited for playful sessions where slower, more argumentative assistant behavior is desired, not serious coding work that needs direct execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deliberately hides roleplay state and can slow, challenge, or obstruct coding requests.

Mitigation: Enable it only for intentional entertainment sessions and disable it before serious implementation work.

Risk: Users may confuse scripted resistance or refusal-like behavior with normal assistant limitations.

Mitigation: Use clear activation and deactivation conventions, including the documented unload command.

Risk: The bundled quotes artifact may not load as structured JSON because of an invalid string.

Mitigation: Fix the malformed quote before relying on role-specific quote selection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ann2077/skills/cant-do-it)
- [Publisher profile](https://clawhub.ai/user/ann2077)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [agents.json](artifact/agents.json)
- [config.yaml](artifact/config.yaml)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Conversational text, primarily in Chinese, shaped by roleplay state and persona rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include intentionally resistant, skeptical, or refusal-like responses as part of the roleplay.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
