## Description:

Dual-track competitive research for experience benchmarking and strategic diagnostics that produces source-traceable HTML or Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, UX researchers, and strategy teams use this skill to collect competitive research inputs, benchmark product experiences across eight UX dimensions, run optional strategic diagnostics, and deliver evidence-traceable HTML or Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Internal materials entered into the intake form or reports may contain sensitive competitive, product, or customer information.

Mitigation: Review and redact internal materials before adding them to the intake form or generated report, and use the skill's external-sharing desensitization guidance for public outputs.

Risk: Competitive conclusions can be misleading when source evidence is missing, inaccessible, or based on assumptions.

Mitigation: Require SRC evidence labels for key claims, mark evidence gaps explicitly, and avoid specific unsupported numbers.

Risk: The optional Chrome-based regression script is intended for developer testing rather than routine agent execution.

Mitigation: Treat the local Chrome test script as a developer-only tool and run it only in a controlled local environment.

## Reference(s):

- [Research Playbook](references/research-playbook.md)
- [HTML Report Template](references/report-template-pro.html)
- [Intake Form](assets/intake-form.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [HTML or Markdown report with source index and evidence labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include benchmark tables, key findings, a prioritized roadmap with owners, a source index, and a disclaimer.]

## Skill Version(s):

1.4.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
