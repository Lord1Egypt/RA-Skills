## Description: <br>
Parses and validates Chinese Unified Social Credit Codes, checks the checksum, and identifies registration authority, organization type, and registered location from GB 32100-2015 code structure without network access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to validate and explain a Chinese Unified Social Credit Code during contract review, supplier checks, or business-data entry. It provides offline syntactic validation and parsed code components, not live company verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A valid checksum can be mistaken for proof that an organization exists, is legitimate, or is currently in good standing. <br>
Mitigation: Treat results as syntactic validation only and verify business status through authoritative registries when that assurance is needed. <br>
Risk: Parsed administrative region codes can be interpreted as the operating address rather than the registration authority location. <br>
Mitigation: Present region output as registration-location information and avoid using it as evidence of actual business operations. <br>
Risk: Historical or nonstandard license and registration numbers may not fit the GB 32100-2015 unified-code rules. <br>
Mitigation: Report unsupported formats clearly and ask the user to check the original business-license record before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page: China Social Credit](https://clawhub.ai/ToBeWin/china-social-credit) <br>
- [ClawHub publisher profile: ToBeWin](https://clawhub.ai/user/ToBeWin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with validation status, parsed fields, error reasons, and suggested next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline output only; no API key, network lookup, or real-time business-status verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
