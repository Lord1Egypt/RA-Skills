## Description:

Read, write, and manage Lark/Feishu Sheets and download cloud files through the Lark/Feishu OpenAPI, including CSV/JSON export, sheet updates, tab operations, file download, and PDF text/image extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mli-cj](https://clawhub.ai/user/mli-cj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent fetch, export, update, and organize Lark/Feishu spreadsheet data or download shared cloud files for local analysis. It is also useful when downloaded PDFs need text, embedded images, or rendered page images extracted for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored Feishu/Lark app credentials can be used to read, write, or manage spreadsheets and download files available to the app identity.

Mitigation: Use a narrowly permissioned Feishu/Lark app, share only intended sheets or files with the app identity, and avoid broad drive permissions unless they are required.

Risk: Sheet write, add-tab, clone-tab, export, and download operations can change remote content or overwrite local output files.

Mitigation: Confirm the spreadsheet token, sheet ID, range, subcommand, and output path before execution, and use dry-run for mutations before applying changes.

Risk: PDF extraction may install Python packages at runtime.

Mitigation: Run the skill in an isolated environment or preinstall and review the required PDF extraction dependencies before use.

## Reference(s):

- [Lark/Feishu Sheets & Drive OpenAPI Reference](references/lark-sheets-api.md)
- [ClawHub skill page](https://clawhub.ai/mli-cj/skills/feishu-lark-sheets-edit)
- [Publisher profile](https://clawhub.ai/user/mli-cj)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local files such as CSV, JSON, downloaded documents, extracted text, and images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python3 scripts that read local Lark/Feishu app credentials, call Lark/Feishu OpenAPI endpoints, and may write or overwrite user-specified output paths.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
