## Description: <br>
查询车辆位置和车况信息（车锁、车门、车窗、空调等状态）/ Query vehicle location and condition information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzidan](https://clawhub.ai/user/zhouzidan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Tika or Chengqu digital key products installed and bound to their vehicle use this skill to query vehicle location, lock, door, window, A/C, and other status fields through a Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive vehicle location and status data. <br>
Mitigation: Install it only for vehicles bound to the user's own Tika or Chengqu account, and share outputs only with trusted recipients. <br>
Risk: The skill uses a high-sensitivity API key that may grant access to vehicle data. <br>
Mitigation: Prefer setting TIKA_API_KEY in a protected environment, avoid pasting real keys into chat prompts or shared shell history, and clear cached credentials with --clear-auth when access is no longer needed. <br>
Risk: Long-lived local credential cache files can leave residual access on a shared machine. <br>
Mitigation: Use environment variables for routine use when possible; if the cache is used, keep it on a trusted local account and remove ~/.skill_carkey_cache.json after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhouzidan/car-key) <br>
- [Tika Digital Key Website](https://www.tikakey.com/) <br>
- [Chengqu Digital Key Website](https://www.chengqukey.com/) <br>
- [Tika Vehicle Condition API Endpoint](https://openapi.nokeeu.com/iot/v1/condition) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Terminal text summaries or structured JSON from a Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese and English output; can query all data, position only, condition only, detailed status, authentication status, or raw JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
