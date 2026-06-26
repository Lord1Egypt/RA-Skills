## Description: <br>
Browse Bring! shopping app recipe inspirations, including recipe names, authors, types, images, links, tags, filters, and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darkdevelopers](https://clawhub.ai/user/darkdevelopers) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers with Bring! credentials use this skill to discover recipe inspirations, inspect recipe metadata, filter by all or mine tags, and produce JSON for scripting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bring! account credentials are required via environment variables and could be exposed in shared shells, profiles, CI logs, or command history. <br>
Mitigation: Use trusted local shells, avoid storing the password in shared profiles or CI, unset credentials when finished, and rotate the password if exposure is suspected. <br>
Risk: The Bring! Inspirations API returns recipe metadata only, so the skill cannot provide ingredient lists or manage shopping lists directly. <br>
Mitigation: Use the skill for recipe discovery and metadata review only, then verify recipe details before manually adding items elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darkdevelopers/bring-recipes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and Bring! account credentials; recipe browsing is metadata-only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
