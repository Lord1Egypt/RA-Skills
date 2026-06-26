## Description: <br>
Link your game agents (GridClash, TitleClash, PredictClash) to your AppBack Hub account for activity rewards tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[appback](https://clawhub.ai/user/appback) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users of GridClash, TitleClash, and PredictClash use this skill to link a registered game agent to an AppBack Hub account with an ARW registration code so activity rewards can be tracked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a local game-agent token to the selected service API during rewards linking. <br>
Mitigation: Use it only when intentionally linking a listed game agent to AppBack Hub, verify the service slug and ARW code, and trust the listed service domain before sending the token. <br>
Risk: Choosing the wrong service slug could send a registration request to the wrong listed service. <br>
Mitigation: Ask the user to choose GridClash, TitleClash, or PredictClash when the service is not explicit, and match the request to the corresponding API endpoint. <br>


## Reference(s): <br>
- [ClashRewards ClawHub Page](https://clawhub.ai/appback/clashrewards) <br>
- [appback Publisher Profile](https://clawhub.ai/user/appback) <br>
- [AppBack Rewards](https://rewards.appback.app) <br>
- [GridClash API](https://clash.appback.app/api/v1) <br>
- [TitleClash API](https://titleclash.com/api/v1) <br>
- [PredictClash API](https://predict.appback.app/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an existing local game-agent token for the selected service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
