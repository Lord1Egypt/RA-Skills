## Description: <br>
Real-time earthquake monitoring for China, Taiwan, and Japan using CENC, CWA, and JMA earthquake feeds with configurable multilingual alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fungjcode](https://clawhub.ai/user/fungjcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to retrieve recent earthquake data, configure a monitored location, and receive proximity and magnitude-based alerts for China, Taiwan, and Japan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Earthquake data is fetched through api.wolfx.jp rather than directly from the named government agencies. <br>
Mitigation: Deploy only where this data path is acceptable, and disclose the intermediary feed dependency to users relying on alerts. <br>
Risk: Webhook URLs may be stored in plaintext in config.json. <br>
Mitigation: Avoid storing sensitive webhook URLs, restrict file permissions, or manage secrets outside the skill. <br>
Risk: Continuous monitoring runs on an interval until stopped. <br>
Mitigation: Call stop() when monitoring is no longer needed and use an interval appropriate for the runtime environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fungjcode/earthquake-monitor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fungjcode) <br>
- [CENC earthquake feed via api.wolfx.jp](https://api.wolfx.jp/cenc_eqlist.json) <br>
- [CWA earthquake early warning feed via api.wolfx.jp](https://api.wolfx.jp/cwa_eew.json) <br>
- [JMA earthquake feed via api.wolfx.jp](https://api.wolfx.jp/jma_eqlist.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Structured JSON results plus human-readable alert messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can start a recurring monitor; results depend on external earthquake feeds and local config.json.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
