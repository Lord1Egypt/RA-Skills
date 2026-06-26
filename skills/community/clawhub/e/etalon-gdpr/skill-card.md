## Description: <br>
Full GDPR compliance audit for websites and codebases using the local ETALON CLI, including tracker detection, consent checks, privacy policy review, PII data-flow mapping, and compliance report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rednix](https://clawhub.ai/user/rednix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, privacy engineers, and compliance reviewers use this skill to run ETALON CLI audits on websites or local codebases and summarize GDPR-relevant tracker, consent, policy, and PII findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ETALON CLI audits websites and codebases, so scans may access systems or files outside the intended scope if run without authorization. <br>
Mitigation: Run scans only on websites or repositories the user is authorized to audit, and require explicit confirmation before executing scan or audit commands. <br>
Risk: Codebase audits may reveal secrets, credentials, or sensitive configuration values in command output. <br>
Mitigation: Review audit output locally before sharing it and avoid forwarding raw configuration or secret-bearing findings to external tools without explicit approval. <br>
Risk: Optional fix and report-generation commands can write or modify files in a project. <br>
Mitigation: Require separate explicit approval before using --fix or writing generated policy, report, or data-flow files. <br>


## Reference(s): <br>
- [Etalon GDPR Scan on ClawHub](https://clawhub.ai/rednix/etalon-gdpr) <br>
- [ETALON homepage](https://etalon.nma.vc) <br>
- [Publisher profile: rednix](https://clawhub.ai/user/rednix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with shell commands and structured JSON parsed from ETALON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local Markdown policy files, Mermaid data-flow diagrams, or audit reports when the user explicitly requests file output.] <br>

## Skill Version(s): <br>
0.9.6 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
