## Description:

Search, explore, and analyze family history using the FamilySearch API and offline GEDCOM files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keylimesoda](https://clawhub.ai/user/keylimesoda)

### License/Terms of Use:


## Use Case:

External users and genealogy researchers use this skill to search FamilySearch, inspect ancestry and descendant relationships, parse offline GEDCOM files, and turn family tree facts into concise narratives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API mode sends family-history search terms, dates, places, and person IDs to FamilySearch.

Mitigation: Prefer offline GEDCOM mode for private research, and use API mode only when the user intends to query FamilySearch.

Risk: FamilySearch OAuth tokens can grant access to account-linked genealogy data.

Mitigation: Store OAuth tokens through environment variables or the operating system keychain, never usernames or passwords.

Risk: Family history records may include sensitive details about living people.

Mitigation: Avoid including sensitive details about living people unless they are necessary for the user's requested task.

## Reference(s):

- [GEDCOM Format Reference](references/gedcom-format.md)
- [FamilySearch](https://www.familysearch.org)
- [FamilySearch Developers](https://www.familysearch.org/developers/)
- [FamilySearch API](https://api.familysearch.org)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API or GEDCOM query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use live FamilySearch API data when an OAuth token is available, or local GEDCOM files for offline operation.]

## Skill Version(s):

1.0.3 (source: server release evidence, created 2026-02-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
