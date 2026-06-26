## Description: <br>
AI Code Reviewer helps agents review multilingual code for quality, likely bugs, security issues, performance concerns, PR descriptions, and test suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect code changes, summarize review findings, draft PR descriptions, and propose unit tests across common languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private repository code or secrets could be exposed during review. <br>
Mitigation: Confirm where code is sent before use, redact secrets, and avoid sharing unnecessary repository context. <br>
Risk: Generated fixes, PR descriptions, or tests may be incomplete or incorrect. <br>
Mitigation: Review all generated patches, PR text, and test cases before applying or publishing them. <br>
Risk: Optional PR automation may require a GitHub token. <br>
Mitigation: Use a narrowly scoped token and grant only the permissions needed for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/ai-code-reviewer) <br>
- [AI Code Reviewer documentation](https://clawhub.ai/docs/ai-code-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports with code blocks, PR descriptions, test examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked findings, suggested fixes, test cases, checklists, and follow-up review guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
