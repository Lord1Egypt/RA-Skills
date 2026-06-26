## Description: <br>
快速找到板块内的"真龙"，识别龙头股。用于A股短线交易选股。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyp20060323](https://clawhub.ai/user/xuyp20060323) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and market analysts can use this skill to identify likely A-share sector leader stocks during short-term trading workflows. It provides screening criteria for first limit-up signals, order-lock strength, turnover range, theme relevance, and follower-stock exclusion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marked the release suspicious because bundled helper behavior may run nested review actions with broad permissions. <br>
Mitigation: Install only in trusted ClawHub developer or maintainer environments; use --no-yolo or AUTOREVIEW_YOLO=0 for autoreview, and avoid sending diffs containing secrets to fallback reviewers. <br>
Risk: Stock-screening guidance may be incomplete, stale, or unsuitable for a user's trading situation. <br>
Mitigation: Treat the output as decision support only and verify signals, market conditions, and risk controls before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xuyp20060323/a-stock-leader-identification-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/xuyp20060323) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown text with stock-screening criteria and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
