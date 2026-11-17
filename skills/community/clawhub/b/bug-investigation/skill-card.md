## Description:

Systematically reproduces, locates, and diagnoses frontend bugs using steps, hypotheses, DevTools, and minimal repro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to reproduce UI defects, narrow the affected scope, test hypotheses with browser tooling, identify root cause, and produce a structured bug investigation report with repair suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on general debugging language or receive sensitive production data during investigation.

Mitigation: Use sanitized reproduction data, test accounts, logs, screenshots, and network traces instead of real credentials or private production data.

Risk: Fix suggestions based on incomplete reproduction data may be incorrect or too narrow.

Mitigation: Validate the minimal reproduction, review the proposed change, and add targeted regression tests before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/bug-investigation)
- [Project Homepage](https://github.com/wangzhiming1999/oliver-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with checklists, root-cause notes, and optional code snippets or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request sanitized reproduction data, logs, screenshots, browser details, network traces, and test accounts when needed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
