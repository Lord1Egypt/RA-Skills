## Description: <br>
Access weather, IP geolocation, SMS, email, crypto prices, QR codes, Danish CVR, Whois, phone lookup, UUID, stock data, passwords, and more via the API KISS unified gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theill](https://clawhub.ai/user/theill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare authenticated API KISS requests for weather, messaging, lookup, market data, QR code, password, photo, and utility endpoints. It is useful when a workflow needs concise guidance or curl-style examples for a unified third-party API gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMS, flash SMS, and email endpoints can send real messages to external recipients. <br>
Mitigation: Review recipients, subjects, and message bodies before allowing requests to those endpoints. <br>
Risk: The password validation endpoint sends submitted passwords to a third-party service. <br>
Mitigation: Avoid submitting real passwords unless the user explicitly accepts sending them to API KISS. <br>
Risk: Requests send API keys and user-provided parameters to apikiss.com. <br>
Mitigation: Install and use the skill only when the user trusts API KISS with the submitted data and keeps APIKISS_API_KEY in the environment. <br>


## Reference(s): <br>
- [API KISS homepage](https://www.apikiss.com) <br>
- [API KISS API base URL](https://www.apikiss.com/api/v1/) <br>
- [ClawHub skill page](https://clawhub.ai/theill/apikiss) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIKISS_API_KEY for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
