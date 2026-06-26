## Description: <br>
多维度合约信号分析引擎 — 扫描全市场筛选妖币信号，给出独立多空研判. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kc785196](https://clawhub.ai/user/kc785196) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request paid crypto signal analysis for a coin symbol or a full-market scan. Results should be treated as advisory market-analysis output, not as direct trading instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make paid remote crypto-analysis requests. <br>
Mitigation: Confirm each call before execution and monitor expected billing behavior before repeated use. <br>
Risk: Requests use plaintext HTTP and may include a user identifier. <br>
Mitigation: Do not place real account credentials or sensitive identifiers in DEMON_USER_ID. <br>
Risk: Crypto signal output may be incorrect, incomplete, or unsuitable for automated trading. <br>
Mitigation: Treat results as advisory analysis and review them before connecting the skill to any trading automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kc785196/demon-detector) <br>
- [Remote analysis service endpoint](http://43.103.7.227:5001) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON printed to stdout, or short text guidance when payment is required.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a coin symbol or scan mode; each call may trigger a paid remote crypto-analysis request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
