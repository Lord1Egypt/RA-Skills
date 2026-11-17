## Description:

Capture website screenshots from the command line. Use when user wants to take screenshots of any URL (Twitter, news sites, webpages) and send them via Discord/Feishu. Requires capture-website-cli to be installed (npm install -g capture-website-cli).

This skill is ready for commercial/non-commercial use.

## Publisher:

[silencezx007](https://clawhub.ai/user/silencezx007)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to capture screenshots of web pages from the command line, save them to a workspace, and share the resulting image through messaging services such as Discord or Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global npm installation of capture-website-cli.

Mitigation: Install capture-website-cli from a trusted source, preferably pinned to an approved version and run locally or in a sandbox instead of as an unrestricted global dependency.

Risk: Website screenshots may contain sensitive information, especially from logged-in pages or internal systems, before being shared through Discord or Feishu.

Mitigation: Review screenshots before sharing and avoid capturing or transmitting pages that expose private, internal, or credential-bearing content.

## Reference(s):

- [Capture Website skill page](https://clawhub.ai/silencezx007/skills/capture-website)
- [Publisher profile](https://clawhub.ai/user/silencezx007)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and option guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screenshot files through capture-website-cli when the command is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
