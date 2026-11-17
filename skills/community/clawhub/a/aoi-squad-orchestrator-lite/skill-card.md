## Description:

AOI Squad Orchestrator (Lite) helps an agent run preset three-role teams with stable pseudonym team names, renaming options, and a fixed JSON report for each task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to structure a task through a small preset team, inspect or rename role pseudonyms, and receive a parseable task report. It is suited for lightweight planning, writing, implementation outlines, and review workflows where a fixed JSON output is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI stores team nickname mappings in ~/.openclaw/aoi/squad_names.json.

Mitigation: Review, remove, or change that local file when nickname persistence is not desired.

Risk: The generated report_markdown can contain user-provided task text.

Mitigation: Treat report_markdown as untrusted Markdown when displaying it in external renderers, especially renderers that automatically load remote links or images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/aoi-squad-orchestrator-lite)
- [Support issues](https://github.com/edmonddantesj/aoi-skills/issues)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON report with embedded Markdown summary and CLI command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed report schema and stores team nickname mappings locally.]

## Skill Version(s):

0.1.1 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
