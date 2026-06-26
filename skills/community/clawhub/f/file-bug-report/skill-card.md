## Description: <br>
Creates triage-ready OpenClaw bug report drafts by collecting conservative diagnostics, comparing config and plugin state, searching similar issues, and preparing reviewed GitHub issue text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[100yenadmin](https://clawhub.ai/user/100yenadmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and OpenClaw users use this skill to turn slow, broken, unresponsive, tool-starved, or degraded agent reports into reviewed GitHub issue drafts with diagnostics, duplicate-search notes, and explicit unknowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostics and log excerpts can include private paths, prompts, organization names, credentials, or other sensitive local details. <br>
Mitigation: Review every generated file and selected excerpt before sharing; use the skill's redaction and keep private-config, tmp-log, and git-detail collection disabled unless explicitly approved. <br>
Risk: A public GitHub issue or comment can expose unreviewed diagnostics if posted too early. <br>
Mitigation: Keep output as a draft until the user approves the final body and excerpt list, and never upload the full diagnostics directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/100yenadmin/file-bug-report) <br>
- [Issue template](references/issue-template.md) <br>
- [Similar issue search guidance](references/similar-issue-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown issue drafts, diagnostic summaries, reviewed excerpts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft-only public issue text until the user approves posting; generated diagnostics require review before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
