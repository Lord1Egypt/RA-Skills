## Description: <br>
Produces GDPR compliance checklists, scoring guidance, privacy-policy and DPA templates, breach-response checklists, and related command-line reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, compliance teams, and operators can use this skill as a lightweight checklist and template aid for GDPR-related audit, consent, data-rights, breach-response, and DPA workflows. It should not be treated as legal advice, a real security scanner, or an encryption utility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes unsupported security scan and encryption claims that may be mistaken for real assessment or protection. <br>
Mitigation: Use it only as a lightweight checklist or template aid; have qualified legal and security reviewers validate outputs before relying on them. <br>
Risk: Command arguments may be saved locally in the gdpr-checker data directory. <br>
Mitigation: Avoid entering secrets, customer data, breach details, or sensitive operational identifiers; use a controlled GDPR_CHECKER_DIR and clear local logs when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/gdpr-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style reports printed to stdout, with shell command usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output can be redirected to a file; GDPR_CHECKER_DIR changes the local data directory.] <br>

## Skill Version(s): <br>
2.3.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
