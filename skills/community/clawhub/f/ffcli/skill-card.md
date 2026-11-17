## Description:

Query Fireflies.ai meeting data, including meeting search, transcripts, AI summaries, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruigomeseu](https://clawhub.ai/user/ruigomeseu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent query Fireflies.ai meeting data, review transcripts, read AI summaries, extract action items, and inspect account information through ffcli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party CLI that handles Fireflies API credentials and private meeting content.

Mitigation: Review the ffcli npm package or Homebrew tap before installing, prefer a pinned and verified release, and treat transcripts and exported summaries as confidential.

Risk: Fireflies API credentials can be exposed if placed directly in shell history or broad environment scopes.

Mitigation: Use the narrowest Fireflies API key available, configure secrets through the runtime secret mechanism, and avoid pasting API keys directly into shell commands.

## Reference(s):

- [ClawHub Ffcli Skill](https://clawhub.ai/ruigomeseu/skills/ffcli)
- [ffcli npm package](https://www.npmjs.com/package/@ruigomeseu/ffcli)
- [ffcli Homebrew tap](https://github.com/ruigomeseu/homebrew-tap)
- [Fireflies Developer Settings](https://app.fireflies.ai/settings)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands; ffcli command output may be JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffcli and FIREFLIES_API_KEY; may access meeting transcripts, summaries, action items, and account information.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
