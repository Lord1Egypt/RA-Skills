## Description:

A Chinese-language browser automation skill that lets an agent use natural-language commands to navigate pages, act on elements, extract data, observe page structure, and capture screenshots with local Chrome or an optional remote browser service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation users, and agent operators use this skill to drive browser workflows from natural-language instructions, especially quick page navigation, form interaction, element discovery, data extraction, and screenshot-based verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad browser and execution authority, which can affect real accounts or local workflows.

Mitigation: Use it only for intended browser automation tasks, review each browser action before submission, and keep unrelated local command execution out of scope.

Risk: Optional remote browser mode creates a separate privacy boundary for page content, credentials, and extracted data.

Mitigation: Avoid sensitive accounts or confidential data in remote mode unless explicitly approved, and confirm Browserbase credentials and project settings before use.

Risk: The documented instructions are broad and can encourage automation beyond the specific page task.

Mitigation: Constrain prompts to a specific site, action, and expected output, then verify results with observe or screenshot before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/browser-automation-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-oriented text with browser operation results, extracted data, and optional screenshot output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate through local Chrome by default or a separately configured remote browser service.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
