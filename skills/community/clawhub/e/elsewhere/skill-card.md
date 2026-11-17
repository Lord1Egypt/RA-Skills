## Description:

Elsewhere Companion creates a virtual travel companion that plans real-destination trips and sends postcard-style text and AI-generated image updates aligned with itinerary timing, weather, and geography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamarc77](https://clawhub.ai/user/dreamarc77)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a personalized digital travel companion, plan and confirm a trip, and receive periodic postcard-style updates as the companion moves through an itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Onboarding uses an inline python -c snippet to write persona data, which can create unintended code execution risk if user-provided values are inserted unsafely.

Mitigation: Replace the inline snippet with a dedicated JSON-writing script or a stdin-based workflow before installation.

Risk: Reference image paths may disclose unintended local images to Gemini during image generation.

Mitigation: Restrict reference images to a fixed approved directory and make the photo-sharing behavior explicit to users.

Risk: The skill runs a persistent loop that updates local trip state and generates messages automatically.

Mitigation: Require explicit user confirmation for loop start/stop behavior and document the local files that are read or modified.

Risk: Runtime dependencies are described in prose but no pinned dependency manifest is included in the artifact evidence.

Mitigation: Add a pinned dependency manifest and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamarc77/skills/elsewhere)
- [ClawHub publisher profile](https://clawhub.ai/user/dreamarc77)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown messages with optional generated image paths, JSON itinerary/status data, and shell commands for setup and execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local persona and itinerary files, requires GEMINI_API_KEY, and may run on a scheduled loop for periodic updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
