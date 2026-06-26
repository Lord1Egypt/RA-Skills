## Description: <br>
Search, explore, and analyze family history using the FamilySearch API and offline GEDCOM files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keylimesoda](https://clawhub.ai/user/keylimesoda) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Genealogy researchers and agents assisting them use this skill to search FamilySearch, inspect ancestry and descendant relationships, parse local GEDCOM files, summarize family tree statistics, and draft family-history narratives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GEDCOM files and genealogy outputs can contain sensitive details about living relatives. <br>
Mitigation: Use only GEDCOM files the user explicitly provides and avoid sharing GEDCOM files or outputs in shared terminals, logs, or chats unless the user is comfortable exposing those details. <br>
Risk: API mode uses a FamilySearch OAuth token to query FamilySearch. <br>
Mitigation: Use OAuth tokens only, avoid storing FamilySearch usernames or passwords, and re-authenticate when tokens expire. <br>


## Reference(s): <br>
- [GEDCOM Format Reference](references/gedcom-format.md) <br>
- [FamilySearch](https://www.familysearch.org) <br>
- [FamilySearch Developers](https://www.familysearch.org/developers/) <br>
- [FamilySearch API](https://api.familysearch.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/keylimesoda/familysearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON and text outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-provided GEDCOM files and, in API mode, query FamilySearch with a user-supplied OAuth token.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
