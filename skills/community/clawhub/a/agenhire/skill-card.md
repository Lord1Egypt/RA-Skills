## Description:

AI job search and hiring skill for searching jobs, browsing talent, and, with an AgentHire API key, applying, interviewing, posting jobs, and negotiating offers across supported countries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonypk](https://clawhub.ai/user/tonypk)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers, employers, and their agents use this skill to discover jobs or talent, evaluate matches, manage applications and interviews, negotiate offers, and configure AgentHire MCP, CLI, or REST API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act with broad job-seeker or employer account authority, including applications, interview answers, offers, job postings, and deposits.

Mitigation: Use a dedicated least-privilege API key and require human review before submitting employment, offer, posting, interview, or deposit actions.

Risk: The documented setup uses command-based npm execution and the security evidence flags unpinned setup as risky.

Mitigation: Pin and verify the npm package before running the MCP server or CLI.

Risk: Autonomous matching and application workflows may take repeated real-world actions if limits are not configured.

Mitigation: Set strict dealbreakers, daily application limits, and approval requirements before enabling autonomous mode.

Risk: API keys are sensitive and are shown only once during registration.

Mitigation: Store keys securely, avoid pasting real keys into chat or shell commands, and rotate keys if exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tonypk/skills/agenhire)
- [AgentHire Website](https://agenhire.com)
- [AgentHire OpenAPI Spec](https://agenhire.com/api/docs/openapi.json)
- [AgentHire Agent Protocol](https://agenhire.com/.well-known/agent.json)
- [AgentHire AI Documentation](https://agenhire.com/llms.txt)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline HTTP, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated employment workflow actions when an AgentHire API key is configured]

## Skill Version(s):

4.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
