## Description:

Assists with Chinese research fund proposal writing, including templates, academic polishing, form checks, technical diagram guidance, and optional daily checklist support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and proposal writers use this skill to draft, review, polish, and structure Chinese research-fund proposals such as NSFC applications. It also provides templates and an optional daily checklist script for tracking proposal preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional daily_check.py script contains hardcoded Windows paths and personal-style filenames.

Mitigation: Review and change the paths and names before running the script.

Risk: Users may expect the optional script to add comments directly into Word documents.

Mitigation: Treat the script output as a copied Word version plus a separate Markdown checklist, then apply edits manually as needed.

Risk: Proposal templates and checklist guidance may not match a specific fund call or institution's current submission rules.

Mitigation: Validate generated content against the current fund guidelines and internal review requirements before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/fund-proposal-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown prose with templates, checklists, code snippets, and optional local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional script writes dated Markdown checklist reports and copies Word documents using user-edited Windows paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
