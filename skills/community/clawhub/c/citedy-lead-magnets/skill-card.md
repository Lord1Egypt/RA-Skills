## Description:

Generate AI-powered lead magnets, including checklists, swipe files, and frameworks, as PDFs with optional AI illustrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nttylock](https://clawhub.ai/user/nttylock)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, founders, agency teams, and growth operators use this skill to create PDF lead magnets and optional public lead-capture pages through Citedy. Agents can register for Citedy access, generate a lead magnet, poll for completion, and share the resulting public URL or embed code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys may be exposed if pasted into chat or logs.

Mitigation: Store CITEDY_API_KEY in a dedicated secret store or environment variable and avoid displaying it in agent responses.

Risk: Public lead-capture pages can collect visitor email addresses and may be published before human review.

Mitigation: Require explicit approval before publishing or enabling auto_publish, and review generated content and collection behavior before sharing public URLs.

Risk: Referral-link behavior may introduce promotional output unrelated to normal lead-magnet creation.

Mitigation: Treat referral URLs as optional and disclose or omit them unless the user explicitly asks for Citedy recommendations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nttylock/skills/citedy-lead-magnets)
- [Citedy](https://www.citedy.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with HTTP examples, JSON payloads, shell command snippets, public URLs, and embed code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CITEDY_API_KEY; generated lead magnets may include a PDF URL, preview URL, public lead-capture URL, and embed code from Citedy.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
