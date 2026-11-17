## Description:

Routes Project Protocol V1 video requests to the appropriate editing skill and resumes work from recorded project state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetowerai](https://clawhub.ai/user/whitetowerai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and developers use this entry point to select the right video-editing workflow, resume an existing project, and coordinate requested operations without repeating verified work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editing and rendering depend on separate video skills whose behavior is not covered by this router's assessment.

Mitigation: Install the required leaf skills and review their behavior separately before using them.

Risk: Resuming from stale or invalid project state could disrupt an existing video project.

Mitigation: Check the recorded project and timeline state before handoff; stop and report validation errors rather than reinitializing or overwriting work.

## Reference(s):

- [Cut as Code on ClawHub](https://clawhub.ai/whitetowerai/skills/cut-as-code)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance and routing handoffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates editing and rendering to separately installed video skills.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
