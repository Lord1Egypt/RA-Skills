## Description:

ACE Music AI音乐LITE helps agents generate MP3 music through the ACE Music API from text prompts, optional lyrics, and instrumental or duration parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent users use this skill to generate short music tracks, custom-lyric songs, or instrumental background audio through ACE Music with local MP3 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an ACE Music API key and could expose credentials if the key is pasted into chat or logs.

Mitigation: Use ACE_MUSIC_API_KEY from the local environment and do not accept, print, store, or commit the key.

Risk: The artifact contains overbroad and inconsistent wording about video editing, media conversion, dubbing, cover songs, and editing existing audio.

Mitigation: Use the skill only for ACE Music text-to-music, custom lyrics, instrumental generation, duration control, and local MP3 output unless the publisher narrows the instructions.

Risk: Generated lyrics or prompts may include sensitive or copyrighted content.

Mitigation: Review prompts and lyrics before submission to the API, and avoid requests involving protected media or cover-song workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ace-music-free)
- [ACE Music API key page](https://acemusic.ai/playground/api-key)
- [ACE Music API endpoint](https://api.acemusic.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples and generated MP3 file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ACE_MUSIC_API_KEY; generated audio is written locally as MP3 files.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
