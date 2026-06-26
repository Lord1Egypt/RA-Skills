## Description: <br>
Build structured company intelligence for interview preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghong5233](https://clawhub.ai/user/wanghong5233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job candidates, recruiters, and interview-preparation agents use this skill to request structured company intelligence for a target company and optional role or job description. It returns company summaries, business direction, technology stack, funding or team-stage signals, interview style, risks, and preparation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, job descriptions, and interview-preparation details may be sent to the local service at 127.0.0.1:8010. <br>
Mitigation: Use the skill only when the local service is trusted, and avoid submitting confidential recruiting material or personal career details unless that service is approved to process them. <br>
Risk: Company intelligence can be incomplete or uncertain. <br>
Mitigation: Preserve confidence and uncertainty in the response, and avoid presenting unsupported company facts as certain. <br>


## Reference(s): <br>
- [Company Intel on ClawHub](https://clawhub.ai/wanghong5233/company-intel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured fields and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls a local HTTP service when company intelligence is requested; asks for the company name when missing and reports API errors without fabricating facts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
