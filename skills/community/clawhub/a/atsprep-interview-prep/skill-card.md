## Description:

Run a mock job interview with ATSPrep's question bank - pick likely questions from the job post and resume, ask them one at a time, and give STAR-based feedback with a stronger version of each answer. Use when someone has an interview coming up, wants likely interview questions, wants to practise answers, or asks to improve a specific answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devabubakar](https://clawhub.ai/user/devabubakar)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to practise interviews tailored to a role or job post, receive one question at a time, and get concise STAR-based feedback grounded in their own answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected resume details, job-post text, or interview answers may be sent to ATSPrep; some rewriting and answer-review tools also use Cloudflare Workers AI.

Mitigation: Tell the user before the first AI transfer, remove unnecessary personal or confidential details, and review the linked privacy guidance.

Risk: ATSPREP_MCP_URL can redirect requests to a different endpoint.

Mitigation: Check any endpoint override before sending user text.

Risk: The remote service's privacy promises have not been independently verified.

Mitigation: Share only text the user is comfortable sending to ATSPrep and its disclosed AI service.

## Reference(s):

- [ATSPrep MCP and tool instructions](references/tools.md)
- [ATSPrep privacy guidance](references/privacy.md)
- [ATSPrep interview questions](https://atsprep.com/tools/interview-questions)
- [ATSPrep MCP endpoint](https://atsprep.com/mcp)
- [ClawHub skill release](https://clawhub.ai/devabubakar/skills/atsprep-interview-prep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text with interview questions, STAR feedback, and suggested answer revisions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks one interview question at a time; suggested answers use only facts the user provided.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
