## Description: <br>
AI code review assistant that analyzes source code and produces review findings, performance suggestions, and security checks across multiple programming languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to review individual files or project directories and produce markdown code review reports with issue summaries, severity levels, and optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package documentation references node scripts/review.mjs, but the release artifact contains only markdown files and no review script. <br>
Mitigation: Before running documented Node commands, confirm that the script exists in the installed skill location and review its contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/code-review-ai) <br>
- [Declared homepage](https://github.com/openclaw/code-review-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and generated review-report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node for the documented review command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
