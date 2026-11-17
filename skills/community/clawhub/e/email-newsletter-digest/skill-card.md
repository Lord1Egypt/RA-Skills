## Description:

Summarizes recent Gmail newsletter emails into a digest using configured labels or sender addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neeravmakwana](https://clawhub.ai/user/neeravmakwana)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to generate, email, schedule, and configure a digest of recent Gmail newsletters. It is useful when recipients want daily newsletter summaries based on configured Gmail labels or sender addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve more Gmail content than selected newsletter messages when fetching full threads for body extraction.

Mitigation: Review configured labels and senders before installation, and be cautious with recurring schedules until full-thread retrieval is acceptable for the mailbox.

Risk: The skill can automatically send digest, warning, or failure emails to configured recipients, including third-party recipients.

Mitigation: Verify recipients and delivery mode before use; prefer individual delivery when recipients should not see each other.

## Reference(s):

- [Email Newsletter Digest Reference](REFERENCE.md)
- [ClawHub Skill Page](https://clawhub.ai/neeravmakwana/skills/email-newsletter-digest)
- [ClawHub Publisher Profile](https://clawhub.ai/user/neeravmakwana)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language status messages, settings JSON updates, and an HTML email digest derived from newsletter summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured labels, senders, recipients, and delivery mode; depends on gog, summarize, and OPENAI_API_KEY.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
