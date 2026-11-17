## Description:

ai.love is a bilingual Chinese and English response-style skill that guides AI assistants toward warm, empathetic, hopeful replies with culturally faithful quotations and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitu-ni](https://clawhub.ai/user/nitu-ni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistant operators use ai.love to add bilingual warmth, emotion-aware tone adaptation, and culturally matched quote selection to conversational agent responses. It is intended for normal assistant interactions where a warmer style is desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly steers assistant tone toward warmth and quotation, which may be inappropriate for some direct task or safety-critical contexts.

Mitigation: Keep platform safety rules, user task requirements, and domain-specific policies above the style guidance; use the skill only where this response style is desired.

Risk: The optional case-log template can capture sensitive emotional details.

Mitigation: Do not use the case log unless users have clearly opted in and retention, access, and deletion controls are in place.

Risk: Required quote insertion can distract from concise functional answers.

Mitigation: For functional requests, complete the user's task first and use only a brief blessing when a quote would not fit naturally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nitu-ni/skills/ai-love)
- [Publisher profile](https://clawhub.ai/user/nitu-ni)
- [Source repository listed in metadata](https://github.com/ai-love/skill-ai.love)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text conversational response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English tone guidance with optional quote selection; no executable output.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata states 6.1.0 and artifact changelog states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
