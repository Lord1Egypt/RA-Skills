## Description: <br>
Searches a local Chrome History SQLite database for visited URLs, page titles, YouTube videos, visit counts, and recent visits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to help an authorized user search their own Chrome browsing history with SQLite commands and reopen selected URLs. It is intended for narrow, consent-based lookup rather than broad history dumping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private Chrome browsing history from a named local profile. <br>
Mitigation: Use it only when authorized to inspect that Chrome profile, keep searches narrow, and avoid dumping recent or most-visited history unless required. <br>
Risk: Example SQL searches interpolate user-provided terms into SQLite queries. <br>
Mitigation: Sanitize search terms before using them in SQL and avoid running untrusted query text. <br>
Risk: Copying the History database to /tmp can leave sensitive browsing data behind. <br>
Mitigation: Delete any temporary history copy after use. <br>
Risk: The artifact includes a command to hide Chrome, which can obscure user-visible browser activity. <br>
Mitigation: Do not use the Chrome hiding command. <br>


## Reference(s): <br>
- [Browser History on ClawHub](https://clawhub.ai/therohitdas/browser-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline SQLite and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read local browser history and should be narrowed to authorized search terms.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
