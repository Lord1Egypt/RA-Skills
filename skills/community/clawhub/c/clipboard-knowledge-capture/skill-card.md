## Description: <br>
Turns supplied clipboard snippets into reviewable local knowledge-base entries with sources, tags, importance notes, follow-up actions, and archive suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and knowledge workers use this skill to turn clipboard text, source notes, and tag intent into structured Markdown or JSON records for a local knowledge base. The skill is designed for reviewable drafts and checklists before any downstream action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive clipboard text could be included in generated notes or output files. <br>
Mitigation: Redact secrets, credentials, personal data, and confidential material before using the skill or saving generated Markdown or JSON. <br>
Risk: Knowledge entries may become hard to verify if source information is missing. <br>
Mitigation: Require source information when capturing a snippet and keep unresolved source gaps in the pending confirmations section. <br>
Risk: The local Python helper can read chosen inputs and write user-selected output files. <br>
Mitigation: Run it only on intended local files, use dry-run or stdout review where appropriate, and avoid changing the bundled spec to inspect broader local paths unless that is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/clipboard-knowledge-capture) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Structured output spec](resources/spec.json) <br>
- [Output template](resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Structured Markdown or JSON, with an optional local Python command for file-based generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sections include excerpt, source, tags, importance, follow-up actions, suggested archive location, pending confirmations, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
