## Description:

Downloads PDF documents from Chaoxing contest and platform viewer URLs, validates page counts, and converts them to TXT with OCR fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artminding](https://clawhub.ai/user/artminding)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help authorized users retrieve Chaoxing viewer PDFs from provided URLs or object IDs, validate expected page counts, and produce searchable TXT extracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download documents without authentication checks, which may be inappropriate for documents the user is not authorized to access.

Mitigation: Use it only for documents the user is authorized to access and review each requested URL before downloading.

Risk: Downloaded PDFs and generated TXT files may persist sensitive document contents in searchable plaintext.

Mitigation: Use a dedicated output directory, restrict access to generated files, and delete outputs when they are no longer needed.

Risk: Untrusted names or batch inputs can affect output destinations or overwrite existing files.

Mitigation: Sanitize filenames, confirm destinations before writing, and avoid overwriting files unless explicitly requested.

Risk: Installing OCR and PDF dependencies into a shared environment can add avoidable supply-chain or environment risk.

Mitigation: Install pinned dependencies in an isolated environment before running conversions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artminding/skills/chaoxing-download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell, Python, and JSON snippets; generated PDF and TXT files when executed by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validates reported page counts and labels OCR-derived or empty pages in TXT output.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
