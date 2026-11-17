## Description:

Captures settled decisions, verified facts, corrections, and reusable procedures from agent sessions into the appropriate wiki pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users capture a few sourced, reusable takeaways from completed tasks or saved sessions in an LLM wiki, rather than storing whole transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session or transcript capture could disclose secrets or private information in a shared wiki.

Mitigation: Choose approved transcript and wiki locations; exclude secret values and information not cleared for wiki readers before filing.

Risk: Unconfirmed or stale session details could be recorded as settled facts or decisions.

Mitigation: Check against the current wiki and source, ask when uncertain, and record only small, dated, sourced items.

## Reference(s):

- [Wiki Capture (Dexio) on ClawHub](https://clawhub.ai/dexio/skills/dexio-wiki-capture)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Small, dated and sourced wiki edits with a brief capture report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Skips duplicates, secrets, and unconfirmed decisions; may produce no wiki edits.]

## Skill Version(s):

1.1.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
