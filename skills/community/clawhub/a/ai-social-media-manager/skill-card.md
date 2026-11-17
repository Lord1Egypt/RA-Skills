## Description:

AI Social Media Manager helps agents plan social content calendars, recommend posting times, draft engagement replies, and summarize performance analytics across multiple social platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, creators, marketers, and agents use this skill to generate posting plans, draft replies, inspect sample analytics, and produce platform-specific social media management guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext account credentials or tokens may be exposed if users follow the documented TOOLS.md credential examples.

Mitigation: Use scoped, revocable secrets through a proper secret manager, and do not store passwords, cookies, API secrets, or access tokens in plaintext documentation.

Risk: Automated replies or publishing workflows can post public content that is wrong, inappropriate, or off-brand.

Mitigation: Require explicit human review and approval before public posting, bulk replies, or automated engagement.

Risk: The artifact makes security claims that are not supported by the server security evidence.

Mitigation: Treat local-only or encrypted-storage claims as unverified until the implementation and credential handling are audited.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/skills/ai-social-media-manager)
- [Artifact README](artifact/README.md)
- [API Documentation](artifact/src/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, CLI text, JSON-like reports, and JavaScript objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include content calendar entries, recommended posting times, drafted replies, analytics summaries, configuration examples, and command examples.]

## Skill Version(s):

1.0.0 (source: server release evidence, package metadata, and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
