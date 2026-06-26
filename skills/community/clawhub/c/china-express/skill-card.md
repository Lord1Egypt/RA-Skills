## Description: <br>
China Express helps agents query Chinese package status through Kuaidi100 browser automation and summarize live tracking results without fallback sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn shipment numbers, delivery messages, or multiple package inputs into current Chinese logistics status summaries sourced from Kuaidi100. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kuaidi100 may require phone-last-four, CAPTCHA, login, slider, or other manual verification before showing live shipment details. <br>
Mitigation: Handle verification prompts manually and report that the query is blocked when verification cannot be completed; do not bypass checks or fabricate tracking status. <br>
Risk: Shipment numbers, logistics messages, and phone-last-four values can include personal delivery information. <br>
Mitigation: Provide only the details needed for the lookup and avoid pasting unrelated personal information. <br>
Risk: Browser automation or page loading failures can leave the agent without current tracking evidence. <br>
Mitigation: Return an explicit unable-to-query message unless the live Kuaidi100 page clearly shows results for the current tracking number. <br>


## Reference(s): <br>
- [China Express on ClawHub](https://clawhub.ai/ToBeWin/china-express) <br>
- [Kuaidi100](https://www.kuaidi100.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese package summaries may include carrier, tracking number, current state, recent events, and explicit blockage messages when live lookup cannot be completed.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
