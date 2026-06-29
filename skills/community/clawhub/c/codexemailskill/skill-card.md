## Description: <br>
Guides agents through repo-aware email implementation, review, auditing, and QA workflows for templates, content systems, and tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan, implement, review, and verify email-related code changes in repositories. It is intended for template edits, React Email work, MDX content changes, QA scripts, codebase diffs, and testable email fixes while keeping live production actions behind explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email workflow guidance could be mistaken for approval to perform live sends or production email-system changes. <br>
Mitigation: Require explicit approval before live sends, contact imports, DNS/authentication changes, suppression edits, provider migrations, destructive cleanup, or production automation changes. <br>
Risk: Template or content edits can introduce rendering regressions, unresolved dynamic fields, or tracking/localization mistakes. <br>
Mitigation: Run the narrowest useful verification, such as render previews, lint, type checks, snapshots, unit tests, or visual smoke checks, and report any verification that could not run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polnikale/codexemailskill) <br>
- [Operating checklist](artifact/references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, file change summaries, QA results, and approval-gated recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repo-aware implementation plans, template diffs, QA scripts, render checks, content patches, concise change reports, and remaining-risk notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
