## Description: <br>
Chinese express tracking skill for querying logistics status and routes across SF Express, YTO, ZTO, STO, Yunda, JD, EMS, and other Chinese carriers without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanyuai](https://clawhub.ai/user/huanyuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese package logistics by tracking number, optionally with a courier code for more accurate carrier selection. It is intended for authorized shipment checks and returns carrier, status, route, and detail-link information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers and phone-number fragments can expose private shipment information. <br>
Mitigation: Use the skill only for shipments the user is authorized to check, and request phone-number fragments only when a carrier requires them. <br>
Risk: The artifact references helper files such as scripts/track.py and references/courier-codes.md that are not included in the packaged evidence. <br>
Mitigation: Verify any referenced helper script or reference file is present and reviewed before allowing an agent to run it. <br>
Risk: Frequent repeated queries may trigger short-term blocking by the logistics data source. <br>
Mitigation: Space repeat tracking queries by more than 30 minutes as documented in the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huanyuai/cn-express-tracker-2) <br>
- [Kuaidi100 logistics data source](https://www.kuaidi100.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command examples and logistics results including carrier, tracking number, current status, route events, and detail link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a courier code for accuracy and, for some SF Express lookups, a phone-number fragment; the artifact recommends spacing repeated queries by more than 30 minutes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
