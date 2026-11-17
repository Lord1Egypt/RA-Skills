## Description:

Search, browse, and open Chrome bookmarks via an AI assistant by reading the local Chrome Bookmarks JSON file directly, without browser extensions or external services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truesnow](https://clawhub.ai/user/truesnow)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers use this skill to search local Chrome bookmarks, browse bookmark folders, inspect bookmark tree structure, and open a selected bookmarked URL from an assistant workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bookmark names, URLs, and folder paths may reveal sensitive personal or internal resources.

Mitigation: Install only when the user is comfortable granting bookmark-read access, and present search results before opening or sharing bookmark details.

Risk: A vague open request can launch the first fuzzy match, which may be the wrong or sensitive bookmark.

Mitigation: Search first for ambiguous names, ask the user to choose an exact result, and avoid broad open commands when bookmarks include sensitive or non-http URLs.

Risk: Opening a bookmark delegates behavior to the operating system and browser for the selected URL scheme.

Mitigation: Confirm the selected URL before opening when the scheme is unusual or when bookmarks may contain internal links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/truesnow/skills/chrome-bookmarks)
- [Skill instructions](artifact/SKILL.md)
- [Chrome Bookmarks CLI script](artifact/scripts/chrome_bookmarks.py)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with bash commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and list commands return bookmark objects; open commands return an opened flag with the selected URL and bookmark name.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
