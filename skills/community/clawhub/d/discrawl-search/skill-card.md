## Description:

Search a user-authorized Discord history archive through discrawl's bounded search and message commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve past Discord conversations from a user-authorized local discrawl archive while keeping message content, identifiers, attachments, and raw payloads private.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results may expose private Discord message content, author identifiers, attachments, or raw payloads from the local archive.

Mitigation: Search only the user-requested scope, keep results private, and avoid sending retrieved content to another channel or service without explicit approval.

Risk: User-provided terms copied into SQL examples could produce unsafe or overbroad local archive queries.

Mitigation: Prefer the bounded discrawl search commands or helper script, validate limits, and reserve SQL for fixed read-only queries authored by the operator.

## Reference(s):

- [Discrawl Database Schema Reference](references/schema.md)
- [Discrawl homepage](https://github.com/openclaw/discrawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and SQL examples; bounded discrawl commands can emit JSON results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches should stay scoped to the user's request and use tight limits, channel filters, or author filters when available.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata, artifact _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
