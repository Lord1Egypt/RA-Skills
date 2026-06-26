## Description: <br>
Looks up address data for a Brazilian CEP using the ViaCEP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guilherme-funchal](https://clawhub.ai/user/guilherme-funchal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Brazilian postal-code address details from CEP values. It returns street, neighborhood, city, state, and complement data when ViaCEP has a matching record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CEP values entered by users are sent to the external ViaCEP service for lookup. <br>
Mitigation: Disclose the external lookup behavior and avoid submitting postal codes the user considers private. <br>
Risk: Lookup results depend on ViaCEP availability and response accuracy. <br>
Mitigation: Handle unavailable, not-found, and failed lookup responses clearly before relying on returned address data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guilherme-funchal/cep-lookup) <br>
- [ViaCEP API](https://viacep.com.br) <br>
- [axios npm package](https://www.npmjs.com/package/axios) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text with labeled address fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes invalid-format, not-found, and network-failure messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
