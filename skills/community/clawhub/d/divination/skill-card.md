## Description:

Provides true-random card, rune, hexagram, dice, and interpretation-prompt draws for divination readings using local shell scripts and reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[and0r](https://clawhub.ai/user/and0r)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to let an agent perform unbiased oracle draws and then interpret the result with tarot, rune, I Ching, Forty Servants, and related reference material. It is intended for spiritual or entertainment readings, not professional medical, mental-health, legal, or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local shell scripts can run unintended commands when crafted numeric inputs are used for dice sizes or impulse counts.

Mitigation: Review the scripts before installation, run them only in a trusted local environment, and validate integer arguments before using user-supplied values.

Risk: Divination readings may be mistaken for medical, mental-health, legal, or financial advice.

Mitigation: Present readings as spiritual or entertainment content and route professional questions to qualified sources.

Risk: Much of the reference material and some script output are in German.

Mitigation: Confirm language expectations before use and translate or summarize German reference passages for readers who need English output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/and0r/skills/divination)
- [The Forty Servants](https://www.adventuresinwoowoo.com/thefortyservants/)
- [Arcane Bullshit Oracle Deck](https://arcanebullshit.com)
- [Forty Servants Cards](references/forty-servants/cards.md)
- [Tarot Major Arcana](references/tarot/major-arcana.md)
- [Tarot Minor Arcana](references/tarot/minor-arcana.md)
- [Elder Futhark Runes](references/runen/elder-futhark.md)
- [I Ching Hexagrams](references/iging/hexagramme.md)
- [Arcane Bullshit Oracle Cards](references/bullshit-tarot/cards.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with shell command examples and plain-text oracle draw outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include German reference text and spiritual or entertainment interpretation language.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
