## Description:

Open Apple News, read Apple News links, and run local News workflows on macOS using deterministic CLI commands and shortcut-based search fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Mac users and agents use this skill to open Apple News, validate and open Apple News article or feed links, and run local reading workflows with explicit confirmation for higher-impact actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed or crafted Apple News links or shortcut names could be passed into local command execution.

Mitigation: Validate Apple News URLs with strict parsing, preview literal arguments before execution, and avoid constructing shell strings from untrusted input.

Risk: Shortcut-based search can trigger user-defined side effects outside the skill's default Apple News flow.

Mitigation: Keep shortcut search opt-in, run only user-owned shortcuts whose side effects are understood, and confirm the shortcut name before execution.

Risk: Opening multiple links or sensitive query terms can expose reading context or disrupt the user's session.

Mitigation: Open one link by default, require explicit confirmation and a second confirmation for multiple links, and store only minimal operational notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/apple-news)
- [Skill homepage](https://clawic.com/skills/apple-news)
- [Apple News endpoint](https://apple.news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-focused; may reference local files under ~/apple-news/ when the user approves persistence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
