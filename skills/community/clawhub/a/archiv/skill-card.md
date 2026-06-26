## Description: <br>
Controls a Roon music system through a local REST API to search a music library and TIDAL, play tracks or albums, manage queues, adjust volume, shuffle, and control playback zones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wegow](https://clawhub.ai/user/wegow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to let an agent operate a Roon music setup through documented REST endpoints for playback, search, queue management, playlists, shuffle, and volume control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes unrelated long-term memory content with credential locations, private local details, and persistence notes. <br>
Mitigation: Remove or sanitize MEMORY.md before installation and keep credentials in environment variables or secure storage instead of skill documentation. <br>
Risk: Broad activation language and playback endpoints can cause live play, queue, volume, or transport changes that interrupt a listening session. <br>
Mitigation: Narrow activation to explicit Roon or music-control requests and confirm disruptive actions such as Play Now, volume changes, and transport controls. <br>
Risk: Hard-coded zone IDs and a local API host may not match the installing user's Roon environment. <br>
Mitigation: Verify and replace zone IDs and the API base URL before issuing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wegow/archiv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint selection guidance, zone configuration details, and live playback-control request examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
