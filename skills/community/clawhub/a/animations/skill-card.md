## Description:

Create performant web animations with proper accessibility and timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose animation techniques, timing, accessibility handling, and web animation libraries for UI work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may add optional animation libraries such as AutoAnimate, Motion, or GSAP while applying the guidance.

Mitigation: Review and approve any new dependencies separately before adding them to a project.

Risk: Motion-heavy UI changes can create accessibility problems for users who request reduced motion.

Mitigation: Apply the skill's prefers-reduced-motion guidance and remove parallax, bouncing, and infinite loops for reduced-motion users.

Risk: Animating layout or paint properties can cause poor runtime performance.

Mitigation: Prefer transform and opacity animations, avoid transition: all, and reserve will-change for specific performance issues.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/animations)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with inline CSS and JSX examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides static animation guidance and does not execute code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
