## Description:

Roll dice using standard tabletop notation (e.g. 2d6+3, 1d20, 4d6kh3). Use when the user asks to roll dice, generate random numbers within a dice-shaped distribution, resolve RPG-style checks, or needs reproducible random rolls via a seed. Supports modifiers and "keep highest" (kh) notation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to resolve tabletop-style dice rolls, RPG checks, and reproducible dice-shaped random outcomes from concise dice notation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extremely large dice expressions can consume excessive local CPU or memory because explicit limits for spec length, dice count, and die sides are not present.

Mitigation: Use locally with reasonable dice expressions, and add explicit limits before exposing the skill to untrusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/dice-roller)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text dice roll results or an integer total in quiet mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional integer seed supports reproducible output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
