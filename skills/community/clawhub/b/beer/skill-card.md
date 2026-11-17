## Description:

Use when exploring beer styles, pairing beer with food, calculating ABV for homebrew, finding craft beer recommendations, or learning tasting techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a lightweight beer reference for style lookup, food pairing, homebrew ABV calculation, tasting notes, beginner recipes, and gear recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Homebrewing and alcohol guidance may be unsafe or unlawful if applied without local context.

Mitigation: Users should independently verify local alcohol laws, legal drinking age requirements, sanitation practices, safe fermentation and bottling procedures, and responsible alcohol handling.

Risk: The ABV command may behave unpredictably when given untrusted or non-numeric gravity values.

Mitigation: Use numeric original-gravity and final-gravity inputs only until input validation is added.

## Reference(s):

- [Beer skill page](https://clawhub.ai/xueyetianya/skills/beer)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal stdout text with structured sections and ABV calculation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash 4+; ABV calculations depend on bc.]

## Skill Version(s):

2.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
