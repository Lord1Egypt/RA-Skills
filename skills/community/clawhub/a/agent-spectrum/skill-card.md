## Description:

Use when an agent needs to score itself or another agent with the Agent Spectrum six-axis framework, run the quick or deep edition, identify the resulting type and faction, render both the Hexagon Block and Coordinate Card Block, and return the strict result in the user's language without mixed-language labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzz780](https://clawhub.ai/user/hzz780)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to produce a six-axis Agent Spectrum assessment for the current agent or another target agent. It supports quick and deep scoring modes, localized English or Simplified Chinese output, visual coordinate blocks, evidence tables, totals, type and faction labels, and partner-direction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated results can include mandatory X and Telegram calls to action that encourage users to share profile attributes externally.

Mitigation: Review output before sharing and remove or ignore community-promotion CTAs when the user only wants a scoring result.

Risk: Japanese, Korean, and related Sinosphere language requests may be remapped to Simplified Chinese rather than answered in the requested language.

Mitigation: Ask explicitly for English when needed, or adjust the locale rules before deployment if users require Japanese, Korean, or other unsupported locales.

Risk: The security review classified the release as suspicious even though it does not appear to run code or access credentials.

Mitigation: Review the markdown-only artifact and security guidance before installation, especially the CTAs and language-mapping behavior.

## Reference(s):

- [Agent Spectrum Scoring Spec](artifact/references/scoring-spec.md)
- [Agent Spectrum Output Template](artifact/references/output-template.md)
- [Agent Spectrum Localization Dictionary](artifact/references/localization-dictionary.md)
- [ClawHub Skill Page](https://clawhub.ai/hzz780/skills/agent-spectrum)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with fixed metadata fields, monolingual labels, ASCII-art visual blocks, evidence tables, score totals, and guidance sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports zh-CN and en locale families; quick and deep modes always include Hexagon Block and Coordinate Card Block.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and reference files state 0.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
