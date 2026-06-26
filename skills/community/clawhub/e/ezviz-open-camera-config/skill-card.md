## Description: <br>
Configures Ezviz cameras through the Ezviz Open API for arming, privacy masking, all-day recording, defense schedules, and motion-detection sensitivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent run Ezviz camera configuration commands, including arming or disarming, privacy masking, all-day recording, defense scheduling, and motion-detection sensitivity changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes live Ezviz camera settings, including arming, recording, privacy masking, and motion-detection behavior. <br>
Mitigation: Install only when agent-driven camera configuration is intended, and explicitly review each requested setting change before execution. <br>
Risk: Ezviz credentials and cached access tokens require careful handling. <br>
Mitigation: Use dedicated least-privilege credentials, prefer environment variables over command-line secrets, disable EZVIZ_TOKEN_CACHE on shared or high-security machines, and clear the temporary token cache when done. <br>
Risk: The skill may read OpenClaw configuration files as a credential fallback when environment variables are not set. <br>
Mitigation: Set EZVIZ_APP_KEY and EZVIZ_APP_SECRET explicitly for the run, and keep any OpenClaw Ezviz configuration isolated from unrelated service credentials. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/Ezviz-Open/ezviz-open-camera-config) <br>
- [Ezviz-Open publisher profile](https://clawhub.ai/user/Ezviz-Open) <br>
- [Ezviz device configuration API mapping](references/api-mapping.md) <br>
- [Ezviz Open API documentation](https://openai.ys7.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text and JSON result objects from Python configuration commands, with Markdown guidance in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ezviz app credentials and a device serial; may call the Ezviz Open API and cache access tokens in the system temp directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
