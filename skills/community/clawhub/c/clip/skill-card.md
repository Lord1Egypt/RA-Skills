## Description:

Downloads a YouTube video, clips the requested start and end time range, and saves the MP4 to ~/Desktop/Clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bestisblessed](https://clawhub.ai/user/bestisblessed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Clip to create short local MP4 clips from YouTube videos by providing a URL, start time, end time, and optional output name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads media from user-supplied URLs and writes clips to ~/Desktop/Clips.

Mitigation: Run it only for URLs you are authorized to download and review the created clip files in the output folder.

Risk: Output names can collide with existing clips.

Mitigation: Use unique clip names for each run to avoid overwriting prior outputs.

Risk: The temporary work directory is predictable.

Mitigation: Avoid running the skill in hostile shared-machine environments.

## Reference(s):

- [Clip ClawHub Skill Page](https://clawhub.ai/bestisblessed/skills/clip)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown with shell command examples and local MP4 file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and ffmpeg; writes clips to ~/Desktop/Clips.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
