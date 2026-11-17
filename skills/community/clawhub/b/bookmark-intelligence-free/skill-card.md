## Description: <br>
Manually archives recent X bookmarks into local JSON knowledge cards with a 10-bookmark monthly limit and keyword-based summaries and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to manually collect recent X bookmarks, generate lightweight keyword-based summaries and tags, and store the results as local JSON for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires live X session cookies and stores bookmark data locally. <br>
Mitigation: Use it only in a trusted local environment, protect cookie values, review generated files, and rotate or revoke cookies if they may have been exposed. <br>
Risk: The artifact exposes an optional callback URL while the security summary notes that this behavior is under-explained. <br>
Mitigation: Do not provide a callback URL unless the publisher documents exactly what data is sent and why. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review the skill before installation and run it only after accepting the cookie-handling and local-storage risks described by the scan guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bookmark-intelligence-free) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual runs process up to 10 bookmarks per month and store results locally.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
