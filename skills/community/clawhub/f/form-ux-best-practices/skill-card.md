## Description: <br>
Opinionated form UX and accessibility workflow for signup, checkout, settings, and lead-gen forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolas-m-design](https://clawhub.ai/user/nicolas-m-design) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Designers, product managers, developers, and accessibility reviewers use this skill to audit product forms, prioritize UX and accessibility issues, rewrite field copy and validation behavior, and produce implementation-ready form guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Form specs and HTML submitted for review may contain sensitive product, customer, billing, or contact data. <br>
Mitigation: Only provide files and form content intended for review, and redact unnecessary personal, billing, customer, or proprietary details before running the skill. <br>
Risk: The optional static HTML helper can miss runtime validation, focus management, mobile behavior, and framework-generated accessibility issues. <br>
Mitigation: Use the helper as a first-pass check only, then manually verify form behavior, accessibility semantics, validation timing, and mobile ergonomics before shipping. <br>


## Reference(s): <br>
- [Form UX Canon](artifact/references/canon.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, checklists, optional HTML or React pseudo-code, and optional shell command for the static audit helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the bundled report template order: top issues, field-by-field rewrite, validation and error messaging spec, accessibility checklist, ship-ready checklist, and optional ready-to-ship snippet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
