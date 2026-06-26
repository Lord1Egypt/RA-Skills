## Description: <br>
Integrates with the Emby Server API to manage media libraries, users, devices, playback sessions, live TV, and encoding settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XuSanHong](https://clawhub.ai/user/XuSanHong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Python-based access to an Emby server and perform library, user, playback, device, live TV, backup, and encoding operations through documented API helper functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships with a real-looking hardcoded API key. <br>
Mitigation: Replace the bundled key before use, rotate it if it could be real, and use a least-privilege Emby account or API key. <br>
Risk: The skill exposes broad server-changing Emby administration actions. <br>
Mitigation: Require explicit user approval before delete, restore, auth-key, user/device, library, encoding, upload, or download actions. <br>
Risk: Download functions can write media or images to local paths. <br>
Mitigation: Keep saved media in a dedicated folder to reduce accidental overwrite of important files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/XuSanHong/emby) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Emby API wrapper source](artifact/emby.py) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance, API calls, files] <br>
**Output Format:** [Python functions returning JSON dictionaries, response objects, bytes, or saved media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BASE_URL and API_KEY configuration before use; selected functions can modify the target Emby server or write downloaded media to disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
