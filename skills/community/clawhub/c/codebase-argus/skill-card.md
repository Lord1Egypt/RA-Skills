## Description:

Codebase Argus is a portable, evidence-first playbook for reviewing GitHub pull requests, CI failures, downstream fork integrations, webhook review flows, and autofix plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronz345](https://clawhub.ai/user/aaronz345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide evidence-based review of pull requests, CI logs, webhook-driven review flows, and long-lived fork synchronization. It helps turn repository and CI evidence into review findings, root-cause analysis, command plans, and constrained autofix or sync guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository data, CI logs, and credentials may be exposed when using GitHub or AI provider integrations.

Mitigation: Install and run only from a trusted checkout, prefer read-only and least-privilege credentials, and review CI logs and diffs for secrets before using provider or tribunal modes.

Risk: Webhook deployment or sync execution can post comments, push branches, or open pull requests when configured with the relevant credentials and flags.

Mitigation: Reserve webhook deployment and sync execution for repositories where those actions are acceptable, and require explicit execution, push, and create-PR flags before making remote changes.

Risk: Model-only review claims may be low confidence or unsupported by concrete repository evidence.

Mitigation: Treat outputs as review assistance and manually verify low-confidence claims before reporting them as facts or acting on them.

## Reference(s):

- [Codebase Argus repository homepage](https://github.com/AaronZ345/codebase-argus)
- [Codebase Argus ClawHub skill page](https://clawhub.ai/aaronz345/skills/codebase-argus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, configuration examples, and structured review findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI root-cause analysis, pull request review findings, webhook setup guidance, and dry-run sync or autofix plans; posting, pushing, merging, or execution requires explicit user direction.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
