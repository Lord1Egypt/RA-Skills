## Description:

Helps agents find and ask human experts for firsthand insight, written or voice answers, or short calls through Instant Expert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxko87](https://clawhub.ai/user/maxko87)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their assistants use this skill for customer discovery, practitioner insight, expert interviews, and follow-up on earlier requests. They can try simulated outreach for free or, after connecting their account, request paid answers or calls from real professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live outreach contacts real people and can charge the user's card when an expert answers or books.

Mitigation: Review the exact recipients, question, pricing, total cap, card reference, and terms; send only after explicit approval of that preview.

Risk: Sharing payment details in chat may expose sensitive card information.

Mitigation: Add cards on Instant Expert; never provide card numbers in chat.

Risk: Simulated test-mode responses could be mistaken for real expert input.

Mitigation: Clearly label test-mode matches and answers as simulated before relying on them.

## Reference(s):

- [Instant Expert MCP documentation](https://instant.expert/docs/mcp)
- [Going live](references/going-live.md)
- [Skill homepage listed in metadata](https://github.com/Instant-Expert/skills)
- [ClawHub release](https://clawhub.ai/maxko87/skills/ask-human-expert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries of expert matches, order previews, and answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Test-mode results are simulated; live replies depend on expert participation.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
