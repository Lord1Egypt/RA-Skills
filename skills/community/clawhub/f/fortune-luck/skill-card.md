## Description:

Calculates daily fortune readings from a birth date and calendar data, including love, career, wealth, health, lucky elements, and practical suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaferliu](https://clawhub.ai/user/zaferliu)

### License/Terms of Use:

MIT-0

## Use Case:

Users ask an agent to calculate daily fortune readings from a saved or supplied birth date, including Chinese almanac, zodiac, constellation, category scores, lucky elements, and advice. The output is entertainment-style guidance and should not be treated as factual decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store the user's birth date and calendar type locally at ~/.openclaw/fortune_birthday.json.

Mitigation: Use it only when local birthday storage is acceptable, delete the saved file when it is no longer needed, and run under a restricted local account where appropriate.

Risk: Manual installation depends on lunar-python, which may change across versions.

Mitigation: Pin lunar-python to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaferliu/skills/fortune-luck)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, guidance]

**Output Format:** [Plain text, share-style markdown text, or JSON fortune result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a locally saved birthday and calendar type when the user has previously provided them.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
