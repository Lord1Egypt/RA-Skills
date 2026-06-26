## Description: <br>
Write high-converting freelance proposals from job postings (Upwork, Toptal, Freelancer, etc). Given a job URL or pasted description, analyzes the client's real pain point, scores the fit, and writes a 200-word proposal that leads with the solution -- not your resume. Saves connects and increases win rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevdogg102396-afk](https://clawhub.ai/user/kevdogg102396-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers and developers use this skill to evaluate freelance job postings, score fit, and draft targeted proposals that lead with the client's problem and a concrete solution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job descriptions or account context may include private account details, client secrets, or unnecessary sensitive information. <br>
Mitigation: Use pasted job descriptions or WebSearch for job URLs and omit private account details, client secrets, and unrelated sensitive information from job text. <br>
Risk: Fetching job URLs may require shell access when the user asks the agent to retrieve page content. <br>
Mitigation: Allow Bash only when intentionally fetching a page, and review fetched content before using it in a proposal. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with a fit score breakdown, proposal text, and optional follow-up question] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a ready-to-paste 180-220 word proposal or a SKIP recommendation for poor-fit opportunities.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
