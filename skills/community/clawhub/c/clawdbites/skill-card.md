## Description: <br>
Extracts recipes from Instagram reels by parsing captions, transcribing audio, and structuring ingredients, instructions, and macros. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylelol](https://clawhub.ai/user/kylelol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and personal cooking assistants use this skill to turn public Instagram reel links into structured recipes with ingredients, instructions, macros, and source attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download, transcribe, and visually analyze public Instagram reel content. <br>
Mitigation: Use it only with public reels the user intends to process, and disclose that frame analysis may send reel images to the agent's vision model. <br>
Risk: The skill depends on local media-processing tools and a pip-installed Whisper dependency. <br>
Mitigation: Install yt-dlp, ffmpeg, and Whisper only from trusted package sources and keep them updated. <br>
Risk: Optional wishlist or notes actions can persist recipe data. <br>
Mitigation: Save recipes only after the user explicitly chooses a persistent action. <br>
Risk: Estimated ingredient quantities may be inaccurate when the source omits measurements. <br>
Mitigation: Label inferred amounts as estimates and have the user review them before cooking or saving. <br>


## Reference(s): <br>
- [ClawdBites on ClawHub](https://clawhub.ai/kylelol/clawdbites) <br>
- [Clawdbot project](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recipe summaries with ingredients, instructions, macros, source links, and optional JSON wishlist records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include estimated quantities when source media omits measurements; estimates are labeled for user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
