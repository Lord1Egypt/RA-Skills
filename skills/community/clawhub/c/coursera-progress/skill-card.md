## Description: <br>
Fetches and displays Coursera enrollments, course progress, grades, certificates, and upcoming deadlines through Coursera API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ElMoorish](https://clawhub.ai/user/ElMoorish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and agents supporting them use this skill to retrieve Coursera enrollment status, progress, grades, certificates, deadlines, and public course information when appropriate credentials or public endpoints are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to use Coursera client secrets or access tokens to read private enrollment, grade, deadline, and certificate data. <br>
Mitigation: Keep Coursera credentials private, expose them only in intended execution environments, and revoke or rotate them when no longer needed. <br>


## Reference(s): <br>
- [Coursera API key setup](https://www.coursera.org/account/api) <br>
- [Coursera API base URL](https://api.coursera.com/api) <br>
- [ClawHub skill page](https://clawhub.ai/ElMoorish/coursera-progress) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, API URLs, and formatted progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; personal Coursera data requires Coursera API credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
