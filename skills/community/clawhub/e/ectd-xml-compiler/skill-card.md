## Description: <br>
Automatically convert uploaded drug application documents (Word/PDF) into XML skeleton structure compliant with eCTD 4.0/3.2.2 specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Regulatory operations teams and developers can use this skill to turn Word or PDF drug-application draft documents into reviewable eCTD XML skeleton files, module XML, an index, and checksums before expert validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill appears to overstate regulatory compliance and validation for a sensitive drug-submission workflow. <br>
Mitigation: Use generated XML only as a drafting aid, then require expert regulatory review and independent eCTD validation before relying on it for any submission. <br>
Risk: The workflow may process confidential drug-submission files and write outputs to the local workspace. <br>
Mitigation: Run it only in an isolated local environment and avoid shared or uncontrolled workspaces for confidential materials. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ICH eCTD Specification v4.0](https://www.ich.org/page/ectd) <br>
- [FDA eCTD Technical Conformance Guide](https://www.fda.gov/drugs/electronic-regulatory-submission-and-review/ectd-technical-conformance-guide) <br>
- [EMA eSubmission Requirements](https://www.ema.europa.eu/en/human-regulatory/marketing-authorisation/application-procedures/electronic-application-forms) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated XML and checksum files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates eCTD module XML skeletons, index.xml, and index-md5.txt in a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
