## Description:

Runs a Spanish-neutral seven-critic content council that debates a content idea, script, carousel, VSL, or hook and returns a verdict with a viral score, critical risks, rewritten hook and CTA, and prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, and operators use this skill to stress-test content ideas, reels, scripts, carousels, VSLs, hooks, and sales pieces before publishing. It is useful when a user wants multiple conflicting perspectives, a publish/rewrite/kill decision, rewritten opening and CTA copy, and concrete fixes in Spanish-neutral prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can optionally use web, Apify, or Supadata lookups when users provide handles or keywords.

Mitigation: Avoid providing private handles, unreleased campaign details, or sensitive market research unless external lookup is intended.

Risk: The skill may read local brand voice files when they are present.

Mitigation: Review local brand material for sensitive content before making it available to the agent.

Risk: The skill produces opinionated content critique and may generate recommendations that are not appropriate for every brand, audience, or regulated topic.

Mitigation: Have a human reviewer approve rewritten hooks, CTAs, and publishing decisions before using them in live campaigns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/consejo-contenido-formula100k)
- [Skill definition](artifact/SKILL.md)
- [Debate output template](artifact/templates/debate-format.md)
- [Verdict output template](artifact/templates/verdict-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-neutral content critique with a structured debate, publish/rewrite/kill verdict, score, three critical risks, rewritten hook and CTA, five fixes, and one dissenting vote.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
