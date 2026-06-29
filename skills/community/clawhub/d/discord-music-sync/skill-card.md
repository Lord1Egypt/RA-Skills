## Description: <br>
Syncs song lyrics with music playback timing in Discord by generating timed lyric audio segments and synchronized playback instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create karaoke-style Discord playback from timestamped lyrics, including TTS audio segment generation, playback instructions, and timed lyric posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided lyric text may be sent to Minimax TTS and posted into a Discord channel during playback. <br>
Mitigation: Confirm the lyrics are appropriate to share with the selected TTS service and Discord channel before generating or posting them. <br>
Risk: The helper script writes playback files into the output directory chosen by the user. <br>
Mitigation: Use an intended output folder and inspect generated playback files before using them for Discord playback. <br>
Risk: Incorrect or estimated timestamps can cause poorly synchronized karaoke playback. <br>
Mitigation: Review and adjust timestamped lyrics before generating audio segments or sending timed Discord messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/discord-music-sync) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Lyric timing helper script](artifact/scripts/sync_lyrics.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated playback text, TTS audio file instructions, and timed Discord message steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided timed lyrics file, writes playback files to the selected output directory, and can guide TTS generation and Discord posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
