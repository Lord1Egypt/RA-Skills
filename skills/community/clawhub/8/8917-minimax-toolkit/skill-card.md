## Description: <br>
A MiniMax multimodal toolkit that helps agents call official MiniMax APIs for image, speech, voice, video, and music workflows while disclosing quota use, upload boundaries, and output paths before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blicae8917](https://clawhub.ai/user/blicae8917) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production agents use this skill to generate and transform media through MiniMax Token Plan APIs, including image generation, image-to-image, speech, long-text TTS, voice cloning, voice design, and enabled video or music workflows. It is most useful when the agent must estimate request cost, disclose third-party media processing, and save generated files into predictable project directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MiniMax API key and can consume MiniMax Token Plan quota. <br>
Mitigation: Provide credentials only through MINIMAX_API_KEY or the documented OpenClaw config, and review the skill's model and request-cost estimate before execution. <br>
Risk: Prompts, images, audio, or video selected by the user may be uploaded to MiniMax for processing. <br>
Mitigation: Confirm third-party processing is acceptable before submitting sensitive media, and use voice cloning only with permission from the speaker. <br>
Risk: Generated files are saved locally and may include sensitive derived media. <br>
Mitigation: Use --project or --output-dir for isolation, and review the reported save paths after execution. <br>
Risk: Some advertised modalities may be unavailable under the current Token Plan or feature flags. <br>
Mitigation: Check references/feature_flags.json and run the remains or check-docs command before relying on video, template, or music workflows. <br>


## Reference(s): <br>
- [API Info](references/api_info.md) <br>
- [Modalities](references/modalities.md) <br>
- [Budget and Trust Notes](references/budget-and-trust.md) <br>
- [Feature Flags](references/feature_flags.json) <br>
- [Quota Mapping](references/quota_mapping.json) <br>
- [Official Doc Sources](references/official-doc-sources.md) <br>
- [Official Doc Check Report](references/checks/latest-check.md) <br>
- [MiniMax Token Plan FAQ](https://platform.minimaxi.com/docs/token-plan/faq) <br>
- [MiniMax Token Plan Remains API](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, quota estimates, API responses, and saved media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets are saved under an explicit output directory, MINIMAX_OUTPUT_DIR, workspace/03-Resources/minimax-output/, or ./outputs/minimax/, with optional project subdirectories.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
