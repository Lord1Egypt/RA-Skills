## Description: <br>
Controls Ezviz Open Platform PTZ cameras by listing devices, checking status and capabilities, moving PTZ, managing presets, and mirroring camera orientation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to control Ezviz PTZ-capable cameras through the Ezviz Open Platform, including device discovery, status checks, camera movement, preset management, and mirror controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Ezviz camera credentials and access tokens. <br>
Mitigation: Use a dedicated minimal-permission Ezviz app key, prefer environment variables, avoid passing secrets as command-line arguments, and do not print or log tokens. <br>
Risk: Access tokens may be cached on disk in the system temporary directory. <br>
Mitigation: Disable token caching with EZVIZ_TOKEN_CACHE=0 or clear the token cache on shared or high-security machines. <br>
Risk: Mutating PTZ and preset commands can move cameras or change camera state. <br>
Mitigation: Confirm device serials, channels, directions, speeds, and preset actions before running camera-control commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ezviz-Open/ezviz-open-ptz-control) <br>
- [Ezviz Open Platform](https://open.ys7.com/) <br>
- [Ezviz Open API portal](https://openai.ys7.com/) <br>
- [Token API documentation](https://openai.ys7.com/help/81) <br>
- [Device list API documentation](https://openai.ys7.com/help/680) <br>
- [Device status API documentation](https://openai.ys7.com/help/681) <br>
- [Device capacity API documentation](https://openai.ys7.com/help/683) <br>
- [PTZ start API documentation](https://openai.ys7.com/help/690) <br>
- [PTZ stop API documentation](https://openai.ys7.com/help/691) <br>
- [Preset management API documentation](https://openai.ys7.com/help/692) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text with JSON API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EZVIZ_APP_KEY and EZVIZ_APP_SECRET; token caching is controlled by EZVIZ_TOKEN_CACHE.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
