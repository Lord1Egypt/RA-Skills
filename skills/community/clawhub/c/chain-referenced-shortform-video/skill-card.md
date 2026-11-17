## Description:

Guides agents through continuity-preserving shortform AI video planning with shot cards, cinematic blocking, gated keyframes, bridge-frame selection, and chain-referenced generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hakityc](https://clawhub.ai/user/hakityc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and AI video practitioners use this skill to plan short cinematic sequences that preserve character, prop, scene, and camera continuity across shots. It helps convert story beats into shot cards, continuity ledgers, gated keyframe reviews, and chain-referenced video generation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded absolute project paths could make an agent read local source files outside the intended project.

Mitigation: Replace the absolute paths with relative paths or require an explicit project-root confirmation before loading repository-specific files.

Risk: Continuity or shot-planning guidance can still produce unusable video outputs if candidate frames are not reviewed.

Mitigation: Use the skill's master-scene, shot-delta, bridge-frame, and final-clip gates before approving generated sequence clips.

## Reference(s):

- [Film Language For Chain-Referenced Shortform](artifact/references/film-language.md)
- [Repo Mapping For Chain-Referenced Shortform](artifact/references/repo-mapping.md)
- [Review Rubric For Chain-Referenced Shortform](artifact/references/review-rubric.md)
- [ClawHub skill page](https://clawhub.ai/hakityc/skills/chain-referenced-shortform-video)
- [Publisher profile](https://clawhub.ai/user/hakityc)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with structured shot cards, YAML field mappings, continuity review notes, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project-specific planning guidance after relevant files are loaded from an approved project root.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
