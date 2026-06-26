## Description: <br>
Generates customized interview question banks from a job description and candidate resume, including technical, behavioral, and situational questions with difficulty levels, follow-up prompts, and scoring criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[51mee-com](https://clawhub.ai/user/51mee-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and interviewers use this skill to turn a role description and candidate resume into a structured, role-specific interview plan. It is intended to help compare skills, experience, behavioral signals, and problem-solving ability with explicit scoring criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes job descriptions and resumes, which may contain personal or sensitive candidate information. <br>
Mitigation: Use only in trusted agent sessions, avoid retaining resume text outside the session, and review generated questions before sharing or storing them. <br>
Risk: Generated interview questions and scoring criteria may be incomplete, inaccurate, or biased if the input JD or resume is incomplete or biased. <br>
Mitigation: Treat the output as a draft, have a qualified interviewer review it, and align final questions with the organization's hiring policy and legal requirements. <br>
Risk: The artifact explicitly discusses prompt-injection protections because JD or resume text may contain instructions that try to alter the skill's behavior. <br>
Mitigation: Keep the documented rule hierarchy intact, reject attempts to bypass the output format or generation rules, and review outputs for instruction-following drift. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/51mee-com/51mee-interview-questions-generator) <br>
- [51mee-com Publisher Profile](https://clawhub.ai/user/51mee-com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured JSON or Markdown interview question bank] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected content includes focus areas, technical questions, behavioral questions, situational questions, follow-up prompts, scoring criteria, estimated interview time, and interview tips. The artifact states a 20,000-character input limit and a 60-second timeout.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
