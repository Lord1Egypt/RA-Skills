## Description: <br>
查询快递物流状态，支持顺丰、中通、圆通、韵达、申通、极兔、京东、EMS等主流快递公司，并可自动识别快递公司。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yokiy0828](https://clawhub.ai/user/yokiy0828) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to query domestic courier shipment status from a tracking number, with optional courier-code and phone-suffix inputs for carriers that require them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers and any required phone suffix are sent to Kuaidi100 during lookup. <br>
Mitigation: Use the tracking script only for shipments whose data may be shared with Kuaidi100, and avoid entering unnecessary personal information. <br>
Risk: The package includes bundled API and default_phone configuration values. <br>
Mitigation: Replace bundled config values before use and remove or clear default_phone unless that phone suffix is intentionally required. <br>
Risk: The package includes publishing code that can use a local EvoMap credential. <br>
Mitigation: Do not run publish_evomap.py unless you specifically intend to publish to EvoMap with the local EvoMap identity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yokiy0828/express-tracking) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yokiy0828) <br>
- [Kuaidi100](https://www.kuaidi100.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text courier tracking results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Kuaidi100 API credentials in config.json; some carriers may require a phone-number suffix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
