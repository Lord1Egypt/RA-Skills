## Description: <br>
Render a 30-second vertical running-recap video from per-workout data using Remotion, ffmpeg, and royalty-free music for Strava/Garmin-style weekly recap clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn weekly running activity data, GPX tracks, and music into a short shareable MP4 recap for Stories, Twitter, WhatsApp, or marathon-training updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive workout and location data from a local database and Garmin-connected GPX tracks. <br>
Mitigation: Run it only with your own data sources, keep Garmin credentials private, and review generated clips before sharing them. <br>
Risk: The release evidence flags a hard-coded Telegram recipient path for optional delivery. <br>
Mitigation: Remove or replace the Telegram recipient before enabling automated posting or weekly delivery. <br>
Risk: The music guidance includes sources that may require license confirmation before reuse. <br>
Mitigation: Use only tracks with confirmed CC0, public-domain, or compatible licenses and add attribution when a license requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyagil/dyagil-marathon-clip) <br>
- [Royalty-Free Music Sources](references/musical-sources.md) <br>
- [Free Music Archive](https://freemusicarchive.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON/MP4 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workout data JSON, optional GPX-derived track data, and a vertical MP4 recap when run in a configured environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
