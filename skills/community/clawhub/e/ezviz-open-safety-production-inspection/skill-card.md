## Description: <br>
Ezviz safety production inspection skill. Captures device images and sends to Ezviz AI for workplace safety analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run workplace safety inspections from configured Ezviz cameras, including checks for PPE use, falls, cleanliness, and fire or smoke hazards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Ezviz API credentials and may cache access tokens locally. <br>
Mitigation: Use a dedicated minimal-permission Ezviz app, prefer environment variables, and set EZVIZ_TOKEN_CACHE=0 when local token persistence is not acceptable. <br>
Risk: The skill captures camera images and sends them to Ezviz services for remote AI analysis. <br>
Mitigation: Test on non-production devices first, confirm the configured camera scope, and run only where this image flow is permitted. <br>
Risk: The skill may create or reuse Ezviz intelligent agents as part of the inspection workflow. <br>
Mitigation: Review the agent list and template configuration before autonomous use, and require the safety production agent naming rule described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ezviz-Open/ezviz-open-safety-production-inspection) <br>
- [Ezviz-Open publisher profile](https://clawhub.ai/user/Ezviz-Open) <br>
- [Ezviz Open API token endpoint](https://open.ys7.com/api/lapp/token/get) <br>
- [Ezviz device capture endpoint](https://open.ys7.com/api/lapp/device/capture) <br>
- [Ezviz intelligent agent list endpoint](https://open.ys7.com/api/service/open/intelligent/agent/app/list) <br>
- [Ezviz intelligent agent template copy endpoint](https://open.ys7.com/api/service/open/intelligent/agent/template/copy) <br>
- [Ezviz AI analysis endpoint](https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with JSON-formatted analysis results and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ezviz API credentials, configured device serials, network access to Ezviz API domains, and the requests Python package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
