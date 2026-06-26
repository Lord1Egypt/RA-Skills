## Description: <br>
Generate speech audio using Deepdub and attach it as a MEDIA file (Telegram-compatible). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuval-deepdub](https://clawhub.ai/user/yuval-deepdub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to convert text into Deepdub-generated speech audio for delivery as a media attachment, including Telegram-compatible OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthesized text is sent to Deepdub. <br>
Mitigation: Use the skill only with text appropriate for processing by Deepdub under the user's applicable data handling requirements. <br>
Risk: Shared trial credentials are rate-limited and intended only for evaluation. <br>
Mitigation: Use private Deepdub API keys and voice prompt IDs for private or production workloads. <br>
Risk: The Deepdub SDK dependency is not pinned in the artifact. <br>
Mitigation: Pin and review the Deepdub SDK version in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuval-deepdub/deepdub-tts) <br>
- [Deepdub](https://deepdub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [MP3 audio file with a MEDIA path line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audio files to OPENCLAW_MEDIA_DIR and prints MEDIA:<path> for agent consumption.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release metadata; artifact frontmatter/package.json: 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
