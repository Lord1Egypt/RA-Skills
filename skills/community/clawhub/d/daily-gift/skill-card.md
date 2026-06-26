## Description: <br>
Generate personalized, relationship-aware daily gifts in H5, image, video, text, or interactive text-play formats to mark meaningful moments and milestones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiawei248](https://clawhub.ai/user/jiawei248) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to set up a relationship-aware gift engine that can decide whether a day or interaction deserves a gift, then produce and deliver one personalized artifact. It supports onboarding, scheduled daily runs, and manual creative requests across H5, image, video, text, text-play, and hybrid formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled runs can read conversation context and local memory while operating with limited visible user control. <br>
Mitigation: Install only when autonomous daily operation is desired, keep the cron disabled when it is not, and review scheduled delivery settings during setup or reconfiguration. <br>
Risk: The skill stores long-term personal taste, profile, and gift-history records under workspace/daily-gift/. <br>
Mitigation: Review and periodically delete workspace/daily-gift/ data, and avoid placing sensitive personal details in taste or setup files unless they are needed for gift personalization. <br>
Risk: Optional image, video, hosting, audio, and background-removal paths may rely on third-party services and sensitive API credentials. <br>
Mitigation: Prefer environment variables for API keys, avoid storing raw credentials in setup state, and enable only the external providers needed for the selected gift formats. <br>
Risk: Local shell scripts are used for delivery, rendering, deployment, asset retrieval, and post-delivery bookkeeping. <br>
Mitigation: Review scripts before deployment and run the skill in a workspace where local file writes and command execution are acceptable. <br>


## Reference(s): <br>
- [Daily Gift ClawHub Release](https://clawhub.ai/jiawei248/daily-gift) <br>
- [README](README.md) <br>
- [Setup Flow](references/setup-flow.md) <br>
- [Daily Run Flow](references/daily-run-flow.md) <br>
- [Manual Run Flow](references/manual-run-flow.md) <br>
- [Delivery Policy](references/delivery-policy.md) <br>
- [Gift Format Chooser](references/gift-format-chooser.md) <br>
- [Image Integration](references/image-integration.md) <br>
- [Video Integration](references/video-integration.md) <br>
- [Asset Manifest](references/asset-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown delivery messages, HTML/H5 artifacts, generated media briefs, JSON state files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create recurring schedule configuration, local workspace memory, gift history, taste profile records, H5 files, and optional image or video outputs depending on configured services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
