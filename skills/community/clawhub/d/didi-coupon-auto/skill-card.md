## Description: <br>
Automatically opens the Didi coupon page, claims available ride and travel coupons, and reports the coupon details for the user's logged-in Didi session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayue-oss](https://clawhub.ai/user/ayue-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to claim Didi travel coupons on demand or through a daily schedule, then review grouped coupon results for ride-hailing, hitch, chauffeur, train, intercity, and related travel offers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses the user's logged-in Didi browser session to claim coupons. <br>
Mitigation: Install only if comfortable using an authenticated Didi session; use a dedicated browser profile where possible and clear Didi cookies when finished. <br>
Risk: Daily scheduling can run the coupon-claiming flow unattended. <br>
Mitigation: Enable the daily schedule only after deliberate review and disable it when unattended coupon claiming is no longer wanted. <br>
Risk: Local claim logs may contain coupon and account-session activity details. <br>
Mitigation: Delete the skill logs when no longer needed, especially on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayue-oss/didi-coupon-auto) <br>
- [Didi coupon claim page](https://vv.didi.cn/a8ZdG0j?source_id=88446DIDI88446tkmmchild1001&ref_from=dunion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text with grouped coupon summaries and optional JSON log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an OpenClaw browser session connected through the local CDP port.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
