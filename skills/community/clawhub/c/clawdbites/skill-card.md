## Description:

Extract recipes from Instagram reels. Use when a user sends an Instagram reel link and wants to get the recipe from the caption. Parses ingredients, instructions, and macros into a clean format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylelol](https://clawhub.ai/user/kylelol)

### License/Terms of Use:

MIT

## Use Case:

External ClawHub users use this skill to turn public Instagram recipe reels into structured recipes with ingredients, instructions, macros, and source attribution. It can optionally support saving recipe wishlist data for meal-planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically download and analyze public Instagram reel media when a caption is incomplete.

Mitigation: Ask the user before audio or video analysis and limit use to public reels the user is comfortable processing.

Risk: Extracted frames may be sent to the active vision model during fallback analysis.

Mitigation: Disclose frame analysis before use and avoid processing reels that may contain sensitive personal information.

Risk: The installation path includes an unpinned Python package installation for Whisper.

Mitigation: Use pinned versions in an isolated environment and review dependency sources before deployment.

Risk: The artifact behavior uses shared temporary media paths for downloaded video and audio.

Mitigation: Store temporary media in a private per-run directory and clean it up after processing.

## Reference(s):

- [ClawdBites ClawHub listing](https://clawhub.ai/kylelol/skills/clawdbites)
- [kylelol ClawHub publisher profile](https://clawhub.ai/user/kylelol)
- [Clawdbot project](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recipe summary with optional JSON wishlist entries and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inferred ingredient quantities marked as estimated and source attribution to the Instagram reel.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
