## Description: <br>
Context Crumb helps agents cheaply inspect, summarize, and load large prose-heavy local files before deciding what raw source text to read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuchen20](https://clawhub.ai/user/yuchen20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Context Crumb to triage large local natural-language files, such as Markdown docs, notes, transcripts, issue threads, and prose-heavy logs, before loading raw text into LLM context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed output can omit exact wording, syntax, or commands and may mislead if treated as source text. <br>
Mitigation: Use Context Crumb for orientation only, then inspect the original file before quoting, editing, copying commands, or making sensitive decisions. <br>
Risk: The CLI processes local documents that may contain sensitive content. <br>
Mitigation: Install and run it only when comfortable processing those documents locally, and rely on the original source for sensitive or exact text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuchen20/context-crumb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compressed output is for orientation; exact quoting, commands, and edits require checking the original source.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
