## Description: <br>
Checks the authenticity of nationwide VAT invoices by querying the official VAT invoice verification platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serendipity2430](https://clawhub.ai/user/serendipity2430) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to verify Chinese VAT invoice authenticity by opening the national verification site, uploading an invoice file, completing the verification flow, and returning whether the invoice information matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles invoice PDFs and screenshots that may contain sensitive business records. <br>
Mitigation: Require explicit approval for each file upload, restrict access to local files, and delete or protect retained screenshots after use. <br>
Risk: Browser security warnings may be bypassed during automation. <br>
Mitigation: Modify the automation to fail closed on browser security warnings unless the user explicitly approves the destination and session. <br>
Risk: The included patch script can make persistent local changes to the installed skill file. <br>
Mitigation: Remove the patch script or require a user-confirmed backup and review step before applying any local modification. <br>


## Reference(s): <br>
- [ClawHub fp-skill release page](https://clawhub.ai/serendipity2430/fp-skill) <br>
- [Publisher profile](https://clawhub.ai/user/serendipity2430) <br>
- [National VAT invoice verification platform](https://inv-veri.chinatax.gov.cn/fpcygzfw/national-invoice-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Plain text result message with optional local browser screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles invoice PDFs and screenshots as sensitive business records.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
