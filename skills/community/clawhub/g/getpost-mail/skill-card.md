## Description: <br>
Buy shipping labels, get rates, and track parcels via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to sign up for GetPost API access, authenticate with a bearer key, request shipping rates, buy labels, and track parcels through the mail API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buying a shipping label may create a billable transaction or carrier commitment. <br>
Mitigation: Require explicit confirmation of sender, recipient, parcel details, carrier, rate, and total cost before submitting a label purchase. <br>
Risk: The bearer API key grants access to GetPost mail API operations. <br>
Mitigation: Keep the key private, avoid placing it in shared transcripts or files, and prefer test or limited keys if available. <br>
Risk: Rate, label, and tracking requests include address, parcel, and shipment data that may be shared with GetPost and carriers. <br>
Mitigation: Use the skill only with shipping data that is appropriate for GetPost, EasyPost, and carrier processing. <br>
Risk: Pricing, billing, privacy, and carrier-sharing terms may affect whether live use is appropriate. <br>
Mitigation: Verify GetPost's current terms and pricing before using the skill with live shipments. <br>


## Reference(s): <br>
- [GetPost Mail API documentation](https://getpost.dev/docs/api-reference#mail) <br>
- [ClawHub skill page](https://clawhub.ai/dommholland/getpost-mail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API Calls, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GetPost bearer API key; live label purchases can incur cost and share address and parcel data with shipping providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
