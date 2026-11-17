## Description:

Provides command-line wrappers for MiniMax official APIs to generate images, image-to-image outputs, video, speech, long-form TTS, voice clones, voice designs, and music while saving outputs to the workspace or a configured directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blicae8917](https://clawhub.ai/user/blicae8917)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route MiniMax media-generation requests through a consistent CLI, estimate request usage, disclose third-party processing, and save generated outputs in organized workspace or project folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, audio, video, and voice samples may be sent to MiniMax APIs.

Mitigation: Disclose third-party processing before execution and get explicit user acceptance before using sensitive media.

Risk: Voice cloning can misuse a speaker's likeness.

Mitigation: Use voice cloning only with clear permission from the speaker and verify that the account is eligible for the clone workflow.

Risk: The skill reads a MiniMax API key from environment or OpenClaw configuration.

Mitigation: Use a dedicated MiniMax Token Plan key, never hardcode credentials, and rotate the key if it may have been exposed.

Risk: Media downloads and output paths may not have enough containment safeguards.

Mitigation: Use trusted project names and output directories, prefer workspace-contained paths, and avoid sensitive output locations until validation is hardened.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blicae8917/skills/8917-minimax-toolkit)
- [Publisher Profile](https://clawhub.ai/user/blicae8917)
- [MiniMax Token Plan FAQ](https://platform.minimaxi.com/docs/token-plan/faq)
- [MiniMax Token Plan Remains API](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains)
- [MiniMax Toolkit Modalities](references/modalities.md)
- [Budget and Trust Notes](references/budget-and-trust.md)
- [MiniMax API Info](references/api_info.md)
- [Feature Flags](references/feature_flags.json)
- [Official Doc Check Report](references/checks/latest-check.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated media files saved to workspace paths or configured output directories.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; output root priority is --output-dir, MINIMAX_OUTPUT_DIR, workspace/03-Resources/minimax-output/, then ./outputs/minimax/.]

## Skill Version(s):

0.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
