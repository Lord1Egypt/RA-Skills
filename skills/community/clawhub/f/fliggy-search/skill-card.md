## Description:

Search flights, hotels, scenic tickets, and holiday travel products on Fliggy using the Fliggy CLI after checking login state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodermachine](https://clawhub.ai/user/nodermachine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search Fliggy for flights, hotels, scenic tickets, and holiday tours. It helps prepare account-linked CLI searches and summarize travel product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install an unpinned global npm package.

Mitigation: Review the package before installation, install only in a trusted environment, and pin or verify the package version when operational controls require reproducibility.

Risk: The skill creates or reuses a Fliggy login session stored at ~/.fliggy-session.json.

Mitigation: Treat the session file as sensitive account state, avoid sharing or logging it, exclude it from backups, and clear it with fliggy login --clear when no longer needed.

Risk: Searches may be account-linked and can lead toward booking workflows.

Mitigation: Require explicit user confirmation before login, booking, purchase, or other account-linked actions.

Risk: Headless mode can use saved login state or open a browser when login is needed.

Mitigation: Run the CLI in a controlled session and confirm the expected login and browser behavior before allowing background searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nodermachine/skills/fliggy-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on a saved Fliggy session file and headless browser behavior.]

## Skill Version(s):

1.0.2 (source: evidence.json release metadata; artifact/SKILL.md frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
