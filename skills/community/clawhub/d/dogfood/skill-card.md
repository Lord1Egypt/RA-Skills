## Description: <br>
Systematically explores and tests a web application to find bugs, UX issues, console errors, accessibility concerns, and other problems, then produces a structured report with reproducible evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thedalbee](https://clawhub.ai/user/thedalbee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to perform exploratory browser testing of web applications and produce reproducible issue reports with screenshots, videos, console observations, and severity/category labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actively operate a browser against authenticated applications and may trigger state-changing actions during testing. <br>
Mitigation: Run it only on sites you own or are authorized to test, prefer staging or test accounts, set a narrow scope, and explicitly forbid destructive or public-facing changes unless intended. <br>
Risk: Generated auth state, screenshots, videos, console logs, and reports may contain sensitive application or account data. <br>
Mitigation: Store outputs in a controlled location, protect access to generated evidence files, and delete or redact them after review according to the team's data-handling policy. <br>


## Reference(s): <br>
- [Issue Taxonomy](references/issue-taxonomy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thedalbee/dogfood) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with linked screenshot and video evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PNG screenshots, WebM repro videos, console/error observations, and auth-state files when authentication is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
