## Description: <br>
Ezviz restaurant inspection skill. Captures device images and sends to Ezviz AI for food safety analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators, inspection teams, and developers use this skill to capture images from configured Ezviz cameras and request AI-assisted food-safety or restaurant-safety analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Ezviz camera-account access and can capture images from configured devices. <br>
Mitigation: Use a dedicated least-privilege Ezviz account, restrict the configured device list, and test with non-production devices before broader use. <br>
Risk: Captured images are sent to the documented external analysis service. <br>
Mitigation: Run the skill only when image sharing with the Ezviz analysis endpoint is acceptable for the restaurant, privacy, and compliance context. <br>
Risk: Access tokens may be cached persistently under /tmp/ezviz_global_token_cache/. <br>
Mitigation: Review cache handling, rely on restrictive permissions, and disable token caching with EZVIZ_TOKEN_CACHE=0 when the environment requires it. <br>
Risk: The skill may create a remote intelligent agent from a template if no suitable agent exists. <br>
Mitigation: Require explicit operator confirmation before first run and review remote agent creation in the Ezviz account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ezviz-Open/ezviz-open-restaurant-inspection) <br>
- [Ezviz Open token endpoint](https://open.ys7.com/api/lapp/token/get) <br>
- [Ezviz Open capture endpoint](https://open.ys7.com/api/lapp/device/capture) <br>
- [Ezviz intelligent agent analysis endpoint](https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and JSON analysis results with Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ezviz app credentials and one or more configured device serial numbers.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
