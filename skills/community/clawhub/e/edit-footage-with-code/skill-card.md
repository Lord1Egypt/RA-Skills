## Description:

Helps an agent turn raw talking-head footage into a reviewable cut, then add word-timed captions, graphics, and sound with HyperFrames or Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and creators use this skill to review raw footage, produce a clean cut, and add timed visuals or sound before a person reviews the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reported command-injection weakness and unpinned tools could expose shell execution or changed package behavior.

Mitigation: Review shell-command handling and pin or verify external packages before running them.

Risk: Footage or audio may be sent to external services during transcription or editing workflows.

Mitigation: Use local processing where practical, and check the selected service's data terms and obtain consent before uploading media.

Risk: The scan is incomplete because some references could not be resolved.

Mitigation: Resolve and review those references before treating the scan as a complete assessment.

## Reference(s):

- [Skill documentation and declared homepage](https://github.com/vargHQ/skills/tree/main/edit-footage-with-code)
- [Video editing guide](https://varg.ai/how-to/edit-a-video-with-hyperframes-and-agents)
- [HyperFrames workflow notes](references/hyperframes.md)
- [Remotion workflow notes](references/remotion.md)
- [Editing defaults and measurements](references/numbers.md)
- [Research sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [JSON edit lists, shell scripts, code snippets, Markdown review notes, and edited video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft edits are reviewable; a person should inspect frames and listen to the result.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
