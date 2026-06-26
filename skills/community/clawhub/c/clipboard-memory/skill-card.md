## Description: <br>
Recall what the user copied on this Mac via the local clipmem archive: text, commands, URLs, file paths, HTML, images, PDFs, with ranked recall, timeline, search, export, pagination, and filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to recover clipboard items they previously copied, including commands, URLs, snippets, file paths, images, and PDFs. It helps agents query the local clipmem archive before using unrelated web, repository, or filesystem search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/clipboard-memory) <br>
- [Commands Reference](references/commands.md) <br>
- [JSON Schema](references/json-schema.md) <br>
- [Setup Check](references/setup-check.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Worked Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented parsing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires the clipmem binary. Security evidence is clean, but clipboard history may include secrets or private files, so use retention, ignored apps, and API-key filtering where available and require explicit confirmation before exporting raw bytes, deleting history, changing settings, or managing background services.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
