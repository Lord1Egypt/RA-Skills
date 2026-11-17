## Description:

Context Compressor helps agents compress conversation and work logs into structured summaries with batch processing, classification, incremental updates, quality scoring, custom templates, and history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, project managers, and other agent users can use this skill to reduce large agent logs into structured archives for memory management, audits, reporting, and token budget control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags mismatched purpose text, so users may misunderstand whether the skill is for compression, translation, or both.

Mitigation: Review the skill description and intended workflow before installation, and use it only for context-compression tasks that match the documented behavior.

Risk: The skill can read and write local log files and may create classified archives, cache files, history files, and export reports.

Mitigation: Review input and output paths before use, avoid unnecessary sensitive logs, and inspect generated archives, cache, and history files for sensitive content.

Risk: Batch runs, scheduled jobs, exports, and callback destinations can broaden the effect of a single agent action.

Mitigation: Require explicit approval before batch processing, scheduled execution, report export, or use of any callback URL, and allow only trusted HTTPS callback destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/context-compressor-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and structured report formats such as JSON or JSONL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce compressed summaries, classified Markdown archives, cache snapshots, history logs, and export reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
