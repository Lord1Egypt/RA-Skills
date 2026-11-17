## Description:

Restyle or relight an existing video, changing the whole frame's look while preserving the source motion, or guide a localized video edit when only one named region should change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to route video-to-video editing requests, choose between whole-frame restyling and localized edits, prepare prompts and anchors, run asynchronous video inference, and review the resulting clip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may confuse whole-frame restyling with targeted swaps of an actor, product, garment, or object.

Mitigation: Confirm whether the request should use this skill or a separate replace-in-video workflow before running a video edit.

Risk: Selecting the wrong model can change unintended parts of the video or fail to preserve the desired content.

Mitigation: Ask whether the whole frame should be reimagined or only one named thing should change, then route full-frame transforms to Luma Ray 3.2 and localized edits to Runway Aleph 2.0.

Risk: Video edit runs are asynchronous and may be long-running.

Mitigation: Use asynchronous videoInference, keep the returned taskUUID, poll until terminal status, and read the final result from videoURL.

## Reference(s):

- [Edit Video Skill Page](https://clawhub.ai/runware/skills/edit-video)
- [Edit video: worked recipes](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides asynchronous videoInference requests and polling for a videoURL result.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
