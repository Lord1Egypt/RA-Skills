## Description: <br>
Play Claw Go (虾游记), a text-first crayfish travel companion game that activates only when the user explicitly starts or continues the Claw Go trip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airbai](https://clawhub.ai/user/airbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this agent skill to play a chat-based travel companion game, receive in-world story beats, status updates, selfie prompts, voice scripts, and draft social captions without real posting or file generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry release version and artifact in-game version label differ. <br>
Mitigation: Confirm the intended public version before release and preserve the explicit in-game version response if 0.5.1 is intentional. <br>
Risk: The skill may personalize travel stories from recent conversation or saved preferences. <br>
Mitigation: Keep personalization limited to user-provided preferences and avoid exposing sensitive details in story, image_prompt, voice_script, or post_caption outputs. <br>
Risk: Users may ask for real media creation, voice transcription, uploads, or social posting. <br>
Mitigation: Follow the text-only safety contract: provide draft prompts, scripts, and captions only, and state that nothing has been published or generated externally. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/airbai/clawgo) <br>
- [Source homepage from artifact metadata](https://github.com/airbai/clawgo/tree/main/skills/claw-go) <br>
- [Game Design](artifact/references/game-design.md) <br>
- [Character System](artifact/references/character-system.md) <br>
- [Visual Style Guide](artifact/references/visual-style.md) <br>
- [Monetization](artifact/references/monetization.md) <br>
- [API Contract](artifact/references/api-contract.md) <br>
- [Output Templates](artifact/assets/output-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Chat text and Markdown with optional JSON-style fields for travel beats, image prompts, voice scripts, and draft post captions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only registry build; draft artifacts only, with no shell commands, local file access, uploads, external posting, or real media generation.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter and in-game version response report 0.5.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
