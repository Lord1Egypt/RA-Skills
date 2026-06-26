## Description: <br>
Fast package tracking and logistics timeline lookup for 2000+ couriers through BijieServ. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huhao19871026](https://clawhub.ai/user/huhao19871026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check package status, identify couriers, and summarize logistics timelines through BijieServ. It is suited for Chinese and international courier tracking requests where users provide a tracking number and, when required by the carrier, a phone number or route hint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package tracking numbers, phone numbers, route hints, and returned logistics text can reveal shipment or location information. <br>
Mitigation: Provide only the minimum details required by the carrier, use the skill's masking behavior, and review logistics text before sharing it. <br>
Risk: Repeated queries for the same shipment can trigger rate limiting or carrier lockout behavior. <br>
Mitigation: Avoid unnecessary repeat lookups and retry later when the API reports frequent querying or lockout. <br>


## Reference(s): <br>
- [BijieServ Express Query API](https://www.bijieserv.com/api/method/express_app.open.v1.query.exec) <br>
- [BijieServ](https://www.bijieserv.com/) <br>
- [Company Codes](references/company-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tracking summary with package status, latest update, recent timeline, and ETA when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks phone numbers and limits recent timeline output to up to 10 events when using the bundled script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
