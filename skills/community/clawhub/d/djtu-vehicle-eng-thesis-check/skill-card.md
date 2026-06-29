## Description: <br>
Validates DJTU Vehicle Engineering thesis Markdown drafts and builds formatted .docx files when explicitly invoked with /djtu-vehicle-eng-thesis-check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingmaker9](https://clawhub.ai/user/lingmaker9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, reviewers, and developers working with DJTU Vehicle Engineering thesis drafts use this skill to validate required structure, captions, citations, abstract length, and terminology before building a formatted Word document for final review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated .docx may still need institution-specific final adjustments after automated formatting. <br>
Mitigation: Open the Word document for final review and complete the manual checks called out by the skill before submission. <br>
Risk: Environment setup can require installing pandoc with elevated privileges. <br>
Mitigation: Use only the skill's environment check workflow, review any sudo command before running it, and stop if the script reports an unexpected error. <br>


## Reference(s): <br>
- [Source repository](https://github.com/LingMaker9/djtu-vehicle-eng-thesis-check) <br>
- [ClawHub skill page](https://clawhub.ai/lingmaker9/djtu-vehicle-eng-thesis-check) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell command snippets and a generated .docx file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validation output reports line numbers without echoing draft content; the final .docx requires manual Word review.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
