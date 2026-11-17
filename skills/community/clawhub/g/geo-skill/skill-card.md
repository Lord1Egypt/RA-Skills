## Description:

Geo Skill helps industrial park operators prepare AI-readable marketing assets, including llms.txt content, schema templates, question maps, content drafts, diagnostics, and monitoring reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketing teams, and industrial park operators use this skill to structure park information for generative engine discovery, produce AI-friendly content, and draft operational checks for GEO programs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic and monitoring outputs may be mistaken for real measurements even when checks are simulated or unperformed.

Mitigation: Treat generated reports as drafts until the scripts perform real checks and clearly label any simulated data.

Risk: Configuration files and output paths can affect generated files and reports.

Mitigation: Review configuration inputs before use and run scripts with explicit output paths in a controlled workspace.

Risk: Templates may expose park contact or business information in generated public content.

Mitigation: Publish only approved public contact details and review generated content before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/geo-skill)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)
- [clawhub.yaml](artifact/clawhub.yaml)
- [llms.txt Template](artifact/templates/llms.txt)
- [Schema Templates](artifact/templates/schema/)
- [Monitoring Report Template](artifact/templates/monitoring/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JSON-LD, llms.txt, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated llms.txt and report files when the included helper scripts are run with explicit output paths.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact documentation lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
