## Description:

Generates images in Google Flow (labs.google/fx) through browser UI automation, supporting Nano Banana 2 and Nano Banana Pro with landscape and portrait aspect ratios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujuntao123](https://clawhub.ai/user/liujuntao123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit image generation prompts to Google Flow through browser UI automation, including single prompt and batch workflows. It is intended for Flow-based image generation where the user has completed the required consent, runtime, network, and login checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Google authentication data may be extracted and stored locally.

Mitigation: Use a dedicated Chrome profile or test Google account, keep the cookie path out of shared or synced folders, and delete cached credentials after use.

Risk: The npx -y bun fallback can run an unpinned runtime from the package ecosystem.

Mitigation: Prefer a trusted, pinned Bun installation before running the skill.

Risk: Browser UI automation depends on the current Google Flow interface and authenticated session state.

Mitigation: Complete the documented pre-flight checks and verify completion with browser screenshots before treating a generation as finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujuntao123/skills/auto-free-banana)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#auto-free-banana)
- [Google Flow](https://labs.google/fx/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits prompts through the browser UI and relies on browser screenshots to confirm completed image generation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
