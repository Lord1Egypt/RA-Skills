## Description:

Builds a Chinese-language, offline-first local workbench as a strict single-file HTML page for repeated personal workflows, including local save, restore, import, and export behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double6-ai](https://clawhub.ai/user/double6-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent hosts use this skill to turn a clarified recurring personal workflow into a local, offline, single-file workbench. It is suited for personal dashboards, study workbenches, task panels, records, and review tools where user data should stay on the current device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local-deployment guidance may introduce LAN-accessible persistence or scheduled tasks without a clear consent and cleanup boundary.

Mitigation: Review any local-deployment path before use; allow LAN exposure, server-side disk persistence, or scheduled tasks only when explicitly requested, with exact commands, schedule, and disable or removal steps documented.

Risk: The skill runs Python scripts and may invoke Chromium or Playwright for local evaluation.

Mitigation: Install only in an environment where running local Python scripts and browser automation is expected, and review the commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/double6-ai/skills/double6-workbench-builder)
- [OpenClaw homepage metadata](https://github.com/double6-ai/double6-skills/tree/main/skills/double6-workbench-builder)
- [Runtime contract](references/runtime-contract.md)
- [Product schema](references/product.schema.json)
- [Risk packs](references/risk-packs.json)
- [Host integration playbook](references/host-integration-playbook.md)
- [Education rules](references/education-rules.md)
- [Education content research policy](references/education-content-research-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON workflow contracts, and generated single-file HTML artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbenches are local single-file HTML pages; browser evaluation may use Playwright and Chromium when available.]

## Skill Version(s):

0.41.0 (source: frontmatter, manifest, changelog, and server release evidence; released 2026-08-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
