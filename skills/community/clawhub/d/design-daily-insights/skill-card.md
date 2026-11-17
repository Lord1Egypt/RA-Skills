## Description:

Design Daily Insights tracks design tool updates, AI product news, design system evolution, UX research, and design inspiration for bilingual daily digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ellisonnnnnnn](https://clawhub.ai/user/ellisonnnnnnn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, product teams, and developers use this skill to collect recent design and AI product updates, filter and dedupe them, and publish a bilingual digest to chat with an optional temporary web page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The digest web page may be exposed through a temporary public URL.

Mitigation: Serve only an isolated digest directory, avoid private content, and avoid public tunnels when the digest includes sensitive information.

Risk: The publishing flow uses an SSH tunnel and artifact guidance notes weak host-verification safeguards.

Mitigation: Restore SSH host verification before enabling public publishing and know how to stop the server and tunnel.

Risk: Scheduled Feishu or chat delivery can send content to unintended recipients.

Mitigation: Confirm the target channel and schedule before enabling automated delivery.

Risk: The setup script can add all files in the current directory to a Git repository.

Mitigation: Run setup-git.sh only from the intended skill directory after checking that it contains no secrets or unrelated files.

## Reference(s):

- [Source Catalog](references/sources.md)
- [ClawHub Skill Page](https://clawhub.ai/ellisonnnnnnn/skills/design-daily-insights)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Bilingual text and Markdown-style digest with article links, plus generated HTML for a magazine-style web page.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 10-15 curated items, limits the digest to about 2000 Chinese characters, dedupes by URL, and may include a temporary public web URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
