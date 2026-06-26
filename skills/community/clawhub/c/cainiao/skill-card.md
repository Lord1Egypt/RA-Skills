## Description: <br>
Use Cainiao Network for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interpret Cainiao parcel status, find pickup information, compare Cainiao service levels, and estimate delivery timing or fees. It is intended for user-directed logistics questions and should ask only for the shipment or route details needed for the task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cainiao account queries and parcel history may expose personal shipment details such as delivery status, pickup locations, and pickup codes. <br>
Mitigation: Use the skill only for explicit package-tracking tasks, request only necessary details, and avoid disclosing shipment information beyond the user's stated need. <br>
Risk: Local runtime features may persist query history, shipment subscriptions, saved address records, encrypted local files, and privacy exports under the user's OpenClaw data directory. <br>
Mitigation: Disclose local storage paths when privacy is relevant, use persistence only when needed, and direct users to the documented privacy info, clear, and export controls. <br>
Risk: Fee and delivery-time estimates can be inaccurate when live carrier data or confirmed service terms are unavailable. <br>
Mitigation: State assumptions, provide cautious ranges, and avoid claiming that real shipping actions were completed unless live tools are available and confirmed. <br>


## Reference(s): <br>
- [Cainiao skill instructions](artifact/SKILL.md) <br>
- [Cainiao README](artifact/README.md) <br>
- [ClawHub Cainiao skill page](https://clawhub.ai/harrylabsj/cainiao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text responses with shipment status explanations, pickup guidance, service comparisons, and cautious estimates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions when exact fees or delivery times cannot be confirmed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
