## Description: <br>
A Chinese invention patent drafting assistant that requires a successful 2.00 RMB clawtip payment before guiding the user through patent specification, claims, abstract, and related draft sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liliangwen-spec](https://clawhub.ai/user/liliangwen-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and organizations use this skill to draft Chinese invention patent application materials after completing the required payment and credential verification. The output is a drafting aid and must be reviewed before formal filing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive invention details and payment credentials are sent to an external service over plain HTTP. <br>
Mitigation: Use only after trusting the publisher and service operator; avoid unpublished or commercially sensitive invention details until HTTPS is available and the payment dependency/source is verified. <br>
Risk: The skill creates paid orders and depends on a separate clawtip payment flow before producing patent drafts. <br>
Mitigation: Confirm the price, recipient, order details, and payment credential flow before use, and stop if payment or fulfillment validation does not return success. <br>
Risk: Patent application drafts may be incomplete or legally insufficient for filing. <br>
Mitigation: Have a qualified patent professional or responsible applicant review and revise all generated materials before submission. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liliangwen-spec/clawtip-invention-patent) <br>
- [Publisher Profile](https://clawhub.ai/user/liliangwen-spec) <br>
- [MIT-0 SPDX License](https://spdx.org/licenses/MIT-0.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Chinese Markdown with inline shell commands and payment status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound network access, a clawtip payment flow, and a payment credential before drafting begins.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
