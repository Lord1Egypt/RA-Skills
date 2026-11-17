## Description:

Local-first, event-driven RAG for commercial real estate audit and investigation case folders that indexes PDF and Office documents, filters by case and stage, and returns page-level citations for audit workpapers and investigation evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack4world](https://clawhub.ai/user/jack4world)

### License/Terms of Use:


## Use Case:

Audit, investigation, and compliance practitioners use this skill to organize a single case folder, build a local searchable index, and query mixed evidence files with case_id and stage filters. It is intended for local document review workflows that need citations back to source files and PDF pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe Joblib index loading from a user-controlled case path, which can enable local code execution if a malicious index file is selected.

Mitigation: Use only isolated virtual environments, trusted case folders, and trusted index directories; do not query .joblib files supplied or replaceable by others.

Risk: Case values containing path separators may select unintended local index paths before the script validates case IDs.

Mitigation: Use simple case IDs without path separators and review path handling before operational use.

Risk: Unpinned dependency ranges may change behavior or security properties over time.

Mitigation: Pin and hash dependencies before using the skill with sensitive audit evidence.

## Reference(s):

- [Audit Case Folder Template](references/case-folder-template.md)
- [ClawHub skill page](https://clawhub.ai/jack4world/skills/audit-case-rag)
- [ClawHub publisher profile](https://clawhub.ai/user/jack4world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local manifest.jsonl and joblib index files when the bundled script is run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
