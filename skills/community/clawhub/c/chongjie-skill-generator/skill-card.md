## Description: <br>
Generates reusable Skill definitions from natural-language requirements, including skill structure, editable previews, local saving, and optional publishing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to turn natural-language requirements into reusable Skill definitions with names, descriptions, triggers, and Markdown usage guidance. It also supports previewing, saving, and optionally publishing generated skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local skills. <br>
Mitigation: Review generated skill folders and scan their contents before deployment. <br>
Risk: The publish helper can publish whole skill folders through local ClawHub and GitHub accounts, with GitHub repository creation public by default. <br>
Mitigation: Verify active accounts, remove secrets or private prompts, and confirm publication scope before using the publish helper. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chongjie-ran/chongjie-skill-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/chongjie-ran) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown and JSON-like skill definitions with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent local skill files and optional publication artifacts when helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
