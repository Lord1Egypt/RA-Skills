## Description:

Automatically routes requests between local and cloud AI models based on task complexity and privacy, with auto-detection and context tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuldrone](https://clawhub.ai/user/yuldrone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to choose a primary or secondary AI model for a request, favoring local models for sensitive inputs and cloud models for more complex tasks. It supports CLI and Python API workflows for listing models, checking router status, and returning route decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy mode can still route sensitive requests to the configured primary model even when that model is not local.

Mitigation: Verify the primary model is local before using the skill with sensitive inputs, and configure or force routing accordingly.

Risk: Context tracking can store conversation excerpts locally in plaintext.

Mitigation: Disable context recording for sensitive conversations or add redaction and stricter local storage controls before enabling it.

Risk: The documented installer command uses a moving @latest target.

Mitigation: Use a pinned installer version when installing or reproducing this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuldrone/skills/ai-model-router-v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text or JSON route decisions, with Markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit JSON with --json; optional context tracking may write local conversation excerpts under the user's model-router configuration directory.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
