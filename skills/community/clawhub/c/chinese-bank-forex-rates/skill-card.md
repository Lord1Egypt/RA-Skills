## Description: <br>
Fetches the latest public foreign-exchange rates from supported Chinese banks for requested bank and currency names or ISO codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhmcn](https://clawhub.ai/user/lhmcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query current public forex rates from supported Chinese banks and return normalized CNY-per-100-unit buy and sell prices for selected currencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Node.js script makes outbound requests to supported Chinese bank sites for live exchange-rate data. <br>
Mitigation: Run it only where outbound network access to those public bank sites is acceptable, and restrict egress to the documented bank domains in sensitive environments. <br>
Risk: Live bank rate pages or APIs may be unavailable, delayed, or changed by the upstream banks. <br>
Mitigation: Check the returned updateTime and verify rates against bank-published sources before relying on them for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhmcn/chinese-bank-forex-rates) <br>
- [Project homepage listed in package metadata](https://github.com/lhmcn/chinese-bank-forex-rates) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands] <br>
**Output Format:** [JSON object with bankName, updateTime, and a rates array.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rates are normalized to CNY per 100 units of foreign currency; unavailable source values may be returned as empty strings.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
