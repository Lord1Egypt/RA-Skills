## Description:

Expert Toolkit helps agents find, search, and load local expert-role Markdown prompts with Chinese names, category browsing, keyword search, and automatic matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catkid010520](https://clawhub.ai/user/catkid010520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Chinese-speaking agent users use this skill to browse expert categories, search for specialist roles, and load matching local role prompts for tasks such as product planning, architecture review, marketing, data analysis, finance, testing, and support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads Markdown role files from the configured roles directory, so untrusted role files can introduce misleading or unsafe instructions.

Mitigation: Install only trusted role files, keep the roles directory protected from untrusted modification, and review returned prompts before acting on high-impact guidance.

Risk: Setting EXPERT_TOOLKIT_ROLES_ROOT to a broad or private document location may expose unintended local Markdown content to the agent context.

Mitigation: Point EXPERT_TOOLKIT_ROLES_ROOT only at the intended agency-orchestrator roles directory and avoid broad home, workspace, or private-document paths.

Risk: Automatic expert matching is keyword-based and may select an unsuitable expert for ambiguous requests.

Mitigation: For important work, review the matched experts and use explicit expert IDs, category browsing, or search commands when a precise role is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catkid010520/skills/expert-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text containing category lists, search results, selected role prompts, and task guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Markdown role files from a configured roles directory and returns prompt text without network calls, file writes, or persistence.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
