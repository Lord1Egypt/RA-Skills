## Description: <br>
Extracts error patterns from server logs and generates actionable alert rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to analyze server logs, identify repeated error patterns, and draft alert rules with counts, severity labels, regex patterns, and supporting samples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks for an API key without documenting the service, purpose, transmitted data, or key handling. <br>
Mitigation: Do not provide credentials until the publisher documents why they are required and how they are protected. <br>
Risk: Generated alert-rule files may include copied log lines containing tokens, emails, paths, stack traces, or customer identifiers. <br>
Mitigation: Review and redact logs before processing, store generated outputs as sensitive files, and avoid sharing outputs outside approved channels. <br>
Risk: Write behavior is under-documented, so generated files may persist sensitive extracted content. <br>
Mitigation: Use explicit output locations, inspect generated files after each run, and remove sensitive artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangjipeng977/extract-error-patterns) <br>
- [Skill metadata source](https://github.com/MiniMax-AI/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON alert-rule output with extracted pattern counts, severity labels, regex patterns, and sample log lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated alert-rule files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and changelog, released 2026-05-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
