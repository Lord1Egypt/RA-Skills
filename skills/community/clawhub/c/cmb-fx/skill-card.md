## Description: <br>
Queries China Merchants Bank foreign-exchange mid-rate data for HKD-CNY using the disclosed CMB FX rate endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horsley](https://clawhub.ai/user/horsley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent fetch CMB foreign-exchange data, filter for HKD, interpret quote fields, and calculate the HKD-CNY spot mid-rate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to make an outbound network request to the disclosed CMB FX rate endpoint. <br>
Mitigation: Review the endpoint before execution and run the skill only in environments where outbound access to fx.cmbchina.com is acceptable. <br>
Risk: The provided example depends on local command-line tooling. <br>
Mitigation: Confirm curl is installed and install jq or adapt the response filtering before relying on the example command. <br>


## Reference(s): <br>
- [CMB FX Rate API](https://fx.cmbchina.com/api/v1/fx/rate) <br>
- [ClawHub skill page](https://clawhub.ai/horsley/cmb-fx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and exchange-rate calculation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; jq is needed to run the provided filtering example exactly as written.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
