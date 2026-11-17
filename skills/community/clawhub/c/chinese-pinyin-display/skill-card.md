## Description:

Displays Chinese text with pinyin pronunciation in a two-line format for children learning Chinese and pinyin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guytogay](https://clawhub.ai/user/guytogay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and educators can use this skill to have an agent present Chinese responses as aligned pinyin and character lines for children learning pronunciation and literacy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pinyin display mode may persist longer than intended or produce unreadable output if the two-line format is not maintained.

Mitigation: Use the documented exit phrases to return to normal replies and validate that each pinyin line aligns with its matching Chinese-character line.

Risk: Compatible dependency updates allowed by package.json may change pinyin conversion behavior.

Mitigation: Use reproducible installs with the included package-lock.json when consistent output is required.

Risk: Multi-codepoint emoji and some polyphonic characters can produce alignment or pronunciation errors.

Mitigation: Prefer simple emoji in formatted output, run the validation script for examples, and add phrase overrides for ambiguous words when needed.

## Reference(s):

- [Chinese Pinyin Display on ClawHub](https://clawhub.ai/guytogay/skills/chinese-pinyin-display)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Two-line plain text with a pinyin line followed by a Chinese-character line; Markdown may be used for command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual trigger and exit phrases control the display mode. The output relies on pinyin-pro and local phrase overrides, with a validation script for alignment checks.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
