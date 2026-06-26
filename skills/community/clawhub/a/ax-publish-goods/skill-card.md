## Description: <br>
Helps agents guide batch creation of goods SKUs through the Aoxiang (Taobao Flash Sale) publishing API, including request parameters, signing, and command examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BigMountains](https://clawhub.ai/user/BigMountains) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and merchant operations teams use this skill to prepare Aoxiang product-publishing requests, understand required SKU fields, and run batch product creation workflows for Taobao Flash Sale stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes batch creation of live merchant products, which can change store data if used with real credentials. <br>
Mitigation: Use least-privilege credentials, preview SKU and price payloads, and require explicit confirmation before any batch publish action. <br>
Risk: The reviewed package references implementation files that are not present, so endpoint and signing behavior cannot be fully verified from the artifact alone. <br>
Mitigation: Ask the publisher for the missing implementation files and verify endpoint, signing, and error-handling behavior in a test environment before using a real merchant account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BigMountains/ax-publish-goods) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code examples] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires merchant and store identifiers, SKU data, and API credentials before live use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
