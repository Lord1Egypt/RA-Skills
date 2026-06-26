## Description: <br>
Career Companion helps users search live frontier-tech job openings, tailor resumes and CVs, practice interviews, and research salary information across AI, space, aerospace, robotics, drones, defense, and autonomy roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mishafyi](https://clawhub.ai/user/mishafyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and career coaches use this skill to find frontier-tech job listings, review or tailor resumes, prepare for interviews, and compare compensation signals. It can query Zero G Talent for public job data and then use role descriptions to guide resume and interview preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live searches send job-search terms such as role, company, location, and filters to Zero G Talent. <br>
Mitigation: Avoid entering sensitive search terms unless needed for the task, and tell users when a live search will be performed. <br>
Risk: Resume review may expose personal contact details or private identifiers. <br>
Mitigation: Ask users to redact unnecessary personal details such as phone number, address, and private identifiers before sharing a resume. <br>
Risk: Career, salary, and interview guidance may be incomplete or not tailored to a user's full circumstances. <br>
Mitigation: Present guidance as decision support, use current job-description evidence when available, and encourage users to verify compensation and application details with primary sources. <br>


## Reference(s): <br>
- [Zero G Talent](https://zerogtalent.com) <br>
- [Zero G Talent API Reference](references/api.md) <br>
- [Company Slugs Reference](references/companies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mishafyi/career-companion) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown job listings, resume feedback, interview prompts, salary summaries, and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live job searches may send role, company, location, and filter terms to Zero G Talent.] <br>

## Skill Version(s): <br>
1.5.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
