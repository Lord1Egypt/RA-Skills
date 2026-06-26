## Description: <br>
Systematically explores and tests a web application to find bugs, UX issues, and other problems, then produces a structured report with reproduction evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to run exploratory web-app testing from a target URL and collect actionable issue reports with screenshots, videos, console observations, and reproduction steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save login sessions and capture sensitive screenshots or videos during web-app testing. <br>
Mitigation: Use it only on authorized sites, prefer test accounts and test data, choose a safe output directory, and delete auth-state.json plus captured reports, screenshots, videos, and logs after review. <br>
Risk: Exploratory testing on authenticated or production systems may exercise workflows that change data. <br>
Mitigation: Confirm scope before testing, avoid destructive workflows unless explicitly intended, and run against staging or disposable data where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/daxiang-dogfood) <br>
- [Publisher profile](https://clawhub.ai/user/daxiangnaoyang) <br>
- [Issue Taxonomy](references/issue-taxonomy.md) <br>
- [Dogfood Report Template](templates/dogfood-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with linked screenshots, repro videos, issue tables, and concise summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files such as reports, screenshots, videos, console logs, and saved browser authentication state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
