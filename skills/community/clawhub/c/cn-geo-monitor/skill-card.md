## Description: <br>
cn-geo-monitor helps agents plan China-focused AI search optimization for DeepSeek, Kimi, Doubao, Tongyi, and ERNIE by using per-engine citation guidance, brand visibility checks, competitor comparison, content adaptation, and prediction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and brand operators use this skill to evaluate and improve how Chinese brands appear in domestic AI search engines. The skill supports engine-specific content planning, API-backed visibility checks, competitor comparison, and prediction/calibration before publication. <br>

### Deployment Geography for Use: <br>
Global; intended for Chinese AI search optimization workflows. <br>

## Known Risks and Mitigations: <br>
Risk: Brand, competitor, keyword, and content text may be sent to external Tencent Cloud Function API endpoints. <br>
Mitigation: Use the skill only with data approved for external processing, avoid confidential unpublished material, and disclose/confirm network use before running API-backed checks. <br>
Risk: The security evidence reports unsafe script input handling in predict.sh. <br>
Mitigation: Do not run predict.sh on untrusted or adversarial text until payload construction is fixed and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/cn-geo-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/lm203688) <br>
- [Web app free check](https://1341839497-1w5tkesfb0.ap-shanghai.tencentscf.com/) <br>
- [API backend](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with executable shell commands and API-backed analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send brand, competitor, keyword, and content text to external Tencent Cloud Function endpoints.] <br>

## Skill Version(s): <br>
4.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
