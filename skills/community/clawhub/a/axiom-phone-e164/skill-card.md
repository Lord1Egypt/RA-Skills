## Description: <br>
Phone number normalizer that converts user-entered phone numbers to E.164 international format for canonical storage, comparison, and SMS/API formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to normalize phone numbers into a canonical E.164 string for database storage, deduplication, form handling, and SMS or messaging API preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes phone-number shape but does not confirm that a number is reachable or assigned. <br>
Mitigation: Use an authoritative carrier, SMS, or phone-validation service before relying on normalized numbers for deliverability, fraud controls, or compliance decisions. <br>
Risk: Embedded country-code and length rules may not cover every numbering-plan edge case or future change. <br>
Mitigation: Test target geographies against current numbering-plan requirements and update the table before production rollout in new markets. <br>
Risk: Server security guidance warns against relying on standards-compliance claims for security-sensitive workflows without verification. <br>
Mitigation: Validate behavior against the exact standard and workflow requirements before using outputs in security, legal, compliance, signature, OAuth, JWT, or integrity decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiom-phone-e164) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [E.164 strings, JSON parse results, Markdown with inline Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline, deterministic, stdlib-only normalization; does not verify phone-number reachability.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
