## Description:

This skill helps an agent run a Playwright-based search workflow on 裁判文书网, collect court-document metadata and judgment text, and export the results to Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fong12368](https://clawhub.ai/user/fong12368)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals, researchers, and agents use this skill to search Chinese court documents by case cause, region, year, document type, and trial procedure, then gather full judgment text for review in an Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and stores local account and search settings.

Mitigation: Use only an authorized account, run the skill in a private environment, avoid sharing generated configuration files, and enter the password only in a trusted terminal session.

Risk: Bulk collection may trigger service rate limits, account controls, or unauthorized-use concerns.

Mitigation: Prefer test mode or small batches, avoid full-mode bulk runs unless permitted by the service, and follow the built-in delays and stop conditions.

Risk: Exported Excel files may contain sensitive case details, parties, and full judgment text.

Mitigation: Store exported workbooks in an access-controlled location and share them only with authorized recipients.

Risk: The security review reports that the skill under-discloses reading session secrets and decrypting protected responses.

Mitigation: Review the script before installation and execution, and confirm that the decryption and session-secret handling are acceptable for the intended account and use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fong12368/skills/fanghongyuanwenshu)
- [裁判文书网](https://wenshu.court.gov.cn/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown instructions and Python automation that produces Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports a 13-column Excel workbook containing case metadata and cleaned judgment text; long judgment text is truncated before writing to Excel.]

## Skill Version(s):

10.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
