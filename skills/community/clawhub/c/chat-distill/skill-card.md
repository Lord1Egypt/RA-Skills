## Description:

Distill a person's chat style from exported conversation records and generate replies that mimic their voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengqiyu9](https://clawhub.ai/user/mengqiyu9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze authorized chat exports, build a concise profile of a target speaker's messaging style, and generate replies that mimic that linguistic style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat exports may contain private or sensitive personal information.

Mitigation: Use only chat records the user is authorized to analyze, avoid sensitive content where possible, and anonymize private details in reports.

Risk: Mimic replies could be used to impersonate a speaker deceptively.

Mitigation: Use generated replies only with appropriate consent and do not present them as messages written by the original speaker.

## Reference(s):

- [Format Parsers](artifact/references/format-parsers.md)
- [Style Dimensions](artifact/references/style-dimensions.md)
- [Output Templates](artifact/references/output-template.md)
- [ClawHub Skill Page](https://clawhub.ai/mengqiyu9/skills/chat-distill)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown analysis reports, plain-text mimic replies, and optional JSON style profiles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short quoted examples from the supplied chat when they are not sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
