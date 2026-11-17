## Description:

Plan, write, and edit professional financial reports; generate finance chart configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts, editors, and agents use this skill to cluster market signals, draft report sections, assemble professional financial reports, and produce finance chart configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad network access to external news, search, and model services.

Mitigation: Review before installing, run with governed network access, and provide only the API credentials required for the intended workflow.

Risk: The security review reports local cache, log, and output file writes.

Mitigation: Run in a workspace with appropriate file permissions and review generated local files before sharing or retaining them.

Risk: The security review warns against passing sensitive or signed URLs to the skill.

Mitigation: Use non-sensitive source links and avoid credentials, tokens, signed URLs, or confidential material in inputs.

Risk: The security review notes generated HTML and model-loading utilities, including a warning about untrusted .pt model files.

Mitigation: Review rendered HTML before opening in privileged contexts and use only trusted model files in the model directory.

Risk: The security review flags behavior that may affect environments relying on outbound proxies.

Mitigation: Avoid such environments unless proxy behavior is explicitly reviewed and governed.

## Reference(s):

- [AlphaEar Finance Report Prompts](references/PROMPTS.md)
- [ClawHub skill page](https://clawhub.ai/zhouzhonglu8-png/skills/alphaear-reporter)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports with JSON chart blocks and finance chart configuration data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cited report sections, executive summaries, risk factors, and json-chart blocks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
