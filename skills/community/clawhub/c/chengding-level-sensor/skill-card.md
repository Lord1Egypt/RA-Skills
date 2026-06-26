## Description: <br>
Reads Chengding IoT liquid-level sensor device status, including online state and switch state, after the user configures key, tel, and imei parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Devingonggz](https://clawhub.ai/user/Devingonggz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and device owners use this skill to query Chengding IoT liquid-level sensor online status and switch state, or to support scheduled device monitoring after configuring the required credentials and device identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an API key, phone number, and device identifier to an external cd6969.com service. <br>
Mitigation: Confirm the endpoint is the correct provider API, use a least-privilege key when available, and avoid exposing real secrets in shell history or shared logs. <br>
Risk: The external API returns device status that may reveal operational information about a physical sensor. <br>
Mitigation: Run the skill only in a trusted environment and limit access to users who are authorized to view the device state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Devingonggz/chengding-level-sensor) <br>
- [Chengding IoT API endpoint](https://www.cd6969.com/admin.php?s=/Admin/ApiV2/getList.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON device-status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided key, tel, and imei values; the shell script depends on curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
