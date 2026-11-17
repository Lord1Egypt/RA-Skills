## Description:

Render a 30-second vertical (1080x1920) running-recap video from per-workout data using Remotion + ffmpeg + royalty-free music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and runners use this skill to turn Garmin-backed running data into a short weekly recap MP4 with animated stats, GPS map scenes, trends, and music. It is suited for shareable marathon-training updates on Stories, Twitter, WhatsApp, or chat delivery channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Garmin credentials and local fitness data while building GPX tracks and workout summaries.

Mitigation: Use only intended accounts and databases, keep credentials out of generated artifacts, and avoid loading credentials from another project's .env.

Risk: Optional Telegram delivery can send the rendered MP4 to a fixed or unintended recipient.

Mitigation: Remove or replace the hard-coded recipient before use and enable Telegram or cron delivery only after confirming the destination and schedule.

Risk: The rendering pipeline depends on local project paths, Remotion, ffmpeg, headless Chrome, and Node packages.

Mitigation: Pin Remotion locally and verify dependencies, project paths, and generated outputs before relying on scheduled delivery.

## Reference(s):

- [Marathon Clip on ClawHub](https://clawhub.ai/dyagil/skills/dyagil-marathon-clip)
- [Royalty-Free Music Sources](artifact/references/musical-sources.md)
- [Free Music Archive](https://freemusicarchive.org/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, JSON]

**Output Format:** [MP4 file path, terminal output, and generated JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a vertical 1080x1920 H.264/AAC MP4, typically 30-60 seconds, plus data.json and tracks.json intermediates.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
